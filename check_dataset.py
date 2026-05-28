"""
Run this script from your project folder:
    python3 check_dataset.py

It will tell you exactly which students have face images and which don't.
"""
import os
import sqlite3
import cv2
import mediapipe as mp

APP_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(APP_DIR, "attendance.db")
DATASET_DIR = os.path.join(APP_DIR, "dataset")

print("=" * 55)
print("  DATASET DIAGNOSTIC REPORT")
print("=" * 55)

# 1. Check dataset folder exists
if not os.path.exists(DATASET_DIR):
    print(f"❌ dataset/ folder NOT FOUND at: {DATASET_DIR}")
    print("   The app creates this folder, make sure you're running")
    print("   this script from the same directory as app.py")
    exit()

print(f"✅ dataset/ folder found at: {DATASET_DIR}")
print()

# 2. Get students from DB
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()
c.execute("SELECT id, name FROM students ORDER BY id")
students = c.fetchall()
conn.close()

print(f"Students in database: {len(students)}")
print()

# 3. Check each student's folder
detector = mp.solutions.face_detection.FaceDetection(
    model_selection=0, min_detection_confidence=0.5
)

students_with_data = []
students_without_data = []

for sid, name in students:
    folder = os.path.join(DATASET_DIR, str(sid))

    if not os.path.exists(folder):
        print(f"  ❌ ID {sid:3d} | {name:<25} | No folder at dataset/{sid}/")
        students_without_data.append((sid, name))
        continue

    image_files = [f for f in os.listdir(folder)
                   if f.lower().endswith((".jpg", ".jpeg", ".png"))]

    if not image_files:
        print(f"  ❌ ID {sid:3d} | {name:<25} | Folder exists but 0 images")
        students_without_data.append((sid, name))
        continue

    # Check how many have detectable faces
    faces_ok = 0
    for f in image_files:
        img = cv2.imread(os.path.join(folder, f))
        if img is None:
            continue
        results = detector.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        if results.detections:
            faces_ok += 1

    if faces_ok == 0:
        print(f"  ⚠️  ID {sid:3d} | {name:<25} | {len(image_files)} images but 0 faces detected!")
        students_without_data.append((sid, name))
    else:
        print(f"  ✅ ID {sid:3d} | {name:<25} | {faces_ok}/{len(image_files)} images with faces")
        students_with_data.append((sid, name))

detector.close()

print()
print("=" * 55)
print(f"SUMMARY: {len(students_with_data)} ready, {len(students_without_data)} need face photos")
print("=" * 55)

if len(students_with_data) < 2:
    print()
    print("🔴 PROBLEM: Need at least 2 students with face images to train.")
    print("   Go to Add Student → capture face photos for each person.")
elif students_without_data:
    print()
    print("⚠️  These students will NOT be recognized (no face data):")
    for sid, name in students_without_data:
        print(f"   - {name} (ID {sid})")
    print()
    print("   → Go to Add Student and capture their face photos,")
    print("     then click Train Model again.")
else:
    print()
    print("✅ All students have face data. Click 'Train Model' in the app.")
    print("   After training completes, recognition will work for everyone.")