import cv2
import os
import sqlite3
import datetime

from model import load_model_if_exists, predict_with_model, extract_embedding_for_image

# PATHS
APP_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(APP_DIR, "attendance.db")

# Load model
clf = load_model_if_exists()

if clf is None:
    print("❌ Model not trained")
    exit()

# Load face detector
cascade_path = os.path.join(cv2.__path__[0], "data/haarcascade_frontalface_default.xml")
face_cascade = cv2.CascadeClassifier(cascade_path)

# Start camera
cam = cv2.VideoCapture(0)

print("✅ Camera started... Press Q to quit")

while True:
    ret, frame = cam.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        face_img = frame[y:y+h, x:x+w]

        # Convert to embedding
        emb = extract_embedding_for_image(face_img)

        if emb is None:
            continue

        label, conf = predict_with_model(clf, emb)

        if conf < 0.5:
            name = "Unknown"
        else:
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()

            c.execute("SELECT name FROM students WHERE id=?", (int(label),))
            row = c.fetchone()
            name = row[0] if row else "Unknown"

            # ✅ Insert attendance (no duplicate per day)
            today = datetime.datetime.utcnow().date().isoformat()

            c.execute("""
                SELECT * FROM attendance
                WHERE student_id=? AND DATE(timestamp)=?
            """, (int(label), today))

            if not c.fetchone():
                ts = datetime.datetime.utcnow().isoformat()

                c.execute("""
                    INSERT INTO attendance (student_id, name, timestamp)
                    VALUES (?, ?, ?)
                """, (int(label), name, ts))

                conn.commit()

            conn.close()

        # Draw
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)
        cv2.putText(frame, name, (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

    cv2.imshow("Face Attendance", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()