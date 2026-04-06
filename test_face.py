import cv2
import mediapipe as mp

mp_face_detection = mp.solutions.face_detection

img = cv2.imread("test.jpg")

if img is None:
    print("❌ Image not found")
    exit()

img = cv2.resize(img, (640, 480))  # 👈 IMPORTANT

with mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5) as detector:
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = detector.process(img_rgb)

    if results.detections:
        print("✅ Face detected!")
    else:
        print("❌ No face detected")