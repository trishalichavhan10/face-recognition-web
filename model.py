import os
import cv2
import numpy as np
import pickle
import mediapipe as mp
from sklearn.ensemble import RandomForestClassifier

MODEL_PATH = "model.pkl"

# -----------------------------
# FACE DETECTOR (MediaPipe)
# -----------------------------
mp_face = mp.solutions.face_detection.FaceDetection( # type: ignore
    model_selection=1,
    min_detection_confidence=0.5
)

# -----------------------------
# UTIL: Crop face & create embedding
# -----------------------------
def crop_face_and_embed(bgr_image, detection):
    h, w = bgr_image.shape[:2]
    bbox = detection.location_data.relative_bounding_box

    x1 = int(max(0, bbox.xmin * w))
    y1 = int(max(0, bbox.ymin * h))
    x2 = int(min(w, (bbox.xmin + bbox.width) * w))
    y2 = int(min(h, (bbox.ymin + bbox.height) * h))

    if x2 <= x1 or y2 <= y1:
        return None

    face = bgr_image[y1:y2, x1:x2]
    face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
    face = cv2.resize(face, (32, 32), interpolation=cv2.INTER_AREA)

    emb = face.flatten().astype(np.float32) / 255.0
    return emb


# -----------------------------
# LOAD MODEL (IF EXISTS)
# -----------------------------
def load_model_if_exists():
    if not os.path.exists(MODEL_PATH):
        return None
    with open(MODEL_PATH, "rb") as f:
        return pickle.load(f)


# -----------------------------
# PREDICT FACE
# -----------------------------
def predict_with_model(clf, emb):
    proba = clf.predict_proba([emb])[0]
    idx = np.argmax(proba)
    label = clf.classes_[idx]
    confidence = float(proba[idx])
    return label, confidence


# -----------------------------
# TRAIN MODEL (BACKGROUND)
# -----------------------------
def train_model_background(dataset_dir, progress_callback=None):
    """
    dataset/
        student_id/
            img1.jpg
            img2.jpg
    """

    X = []
    y = []

    student_dirs = [
        d for d in os.listdir(dataset_dir)
        if os.path.isdir(os.path.join(dataset_dir, d))
    ]

    total_students = max(1, len(student_dirs))
    processed = 0

    for sid in student_dirs:
        folder = os.path.join(dataset_dir, sid)
        files = [
            f for f in os.listdir(folder)
            if f.lower().endswith((".jpg", ".jpeg", ".png"))
        ]

        for fn in files:
            path = os.path.join(folder, fn)
            img = cv2.imread(path)
            if img is None:
                continue

            results = mp_face.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            if not results.detections:
                continue

            emb = crop_face_and_embed(img, results.detections[0])
            if emb is None:
                continue

            X.append(emb)
            y.append(int(sid))

        processed += 1
        if progress_callback:
            pct = int((processed / total_students) * 80)
            progress_callback(pct, f"Processed {processed}/{total_students} students")

    if len(X) == 0:
        if progress_callback:
            progress_callback(0, "No training data found")
        return

    X = np.array(X)
    y = np.array(y)

    if progress_callback:
        progress_callback(85, "Training RandomForest...")

    clf = RandomForestClassifier(
        n_estimators=150,
        n_jobs=-1,
        random_state=42
    )
    clf.fit(X, y)

    with open(MODEL_PATH, "wb") as f:
        pickle.dump(clf, f)

    if progress_callback:
        progress_callback(100, "Training completed")
