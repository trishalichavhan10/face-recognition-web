import os
import cv2
import numpy as np
import pickle
import mediapipe as mp
from sklearn.ensemble import RandomForestClassifier

MODEL_PATH = "model.pkl"

# ✅ FIXED face detector (no errors)
def get_face_detector():
    return mp.solutions.face_detection.FaceDetection(
        model_selection=1,
        min_detection_confidence=0.5
    )


def crop_face_and_embed(img, detection):
    h, w = img.shape[:2]
    bbox = detection.location_data.relative_bounding_box

    x1 = int(max(0, bbox.xmin * w))
    y1 = int(max(0, bbox.ymin * h))
    x2 = int(min(w, (bbox.xmin + bbox.width) * w))
    y2 = int(min(h, (bbox.ymin + bbox.height) * h))

    if x2 <= x1 or y2 <= y1:
        return None

    face = img[y1:y2, x1:x2]

    if face.size == 0:
        return None

    face = cv2.resize(face, (64, 64))
    face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)

    return face.flatten().astype(np.float32) / 255.0


def extract_embedding_for_image(input_data):
    detector = get_face_detector()

    try:
        # handle file or image
        if hasattr(input_data, "read"):
            file_bytes = np.frombuffer(input_data.read(), np.uint8)
            img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        else:
            img = input_data

        if img is None:
            return None

        # Resize for better and faster detection
        img = cv2.resize(img, (640, 480))

        results = detector.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

        if not results.detections:
            return None

        return crop_face_and_embed(img, results.detections[0])
    finally:
        detector.close()


def load_model_if_exists():
    if not os.path.exists(MODEL_PATH):
        return None
    with open(MODEL_PATH, "rb") as f:
        return pickle.load(f)


def predict_with_model(clf, emb):
    proba = clf.predict_proba([emb])[0]
    idx = np.argmax(proba)
    return clf.classes_[idx], float(proba[idx])


def train_model_background(dataset_dir, progress_callback=None):
    detector = get_face_detector()

    X, y = [], []

    try:
        for sid in os.listdir(dataset_dir):
            folder = os.path.join(dataset_dir, sid)
            if not os.path.isdir(folder):
                continue

            for file in os.listdir(folder):
                if not file.lower().endswith((".jpg", ".png", ".jpeg")):
                    continue

                img = cv2.imread(os.path.join(folder, file))
                if img is None:
                    continue

                # Resize image for consistency
                img = cv2.resize(img, (640, 480))

                results = detector.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
                if not results.detections:
                    continue

                emb = crop_face_and_embed(img, results.detections[0])
                if emb is not None:
                    X.append(emb)
                    y.append(int(sid))
    finally:
        detector.close()

    if not X:
        if progress_callback:
            progress_callback(0, "No data")
        return

    clf = RandomForestClassifier(n_estimators=200)
    clf.fit(np.array(X), np.array(y))

    with open(MODEL_PATH, "wb") as f:
        pickle.dump(clf, f)

    if progress_callback:
        progress_callback(100, "Training complete")