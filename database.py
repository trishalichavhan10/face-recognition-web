import sqlite3
import os
import datetime

APP_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(APP_DIR, "attendance.db")


def create_tables():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            name TEXT,
            timestamp TEXT
        )
    """)

    conn.commit()
    conn.close()


def insert_attendance(student_id, name):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    today = datetime.datetime.utcnow().date().isoformat()

    # Check duplicate
    c.execute("""
        SELECT * FROM attendance
        WHERE student_id=? AND DATE(timestamp)=?
    """, (student_id, today))

    if not c.fetchone():
        ts = datetime.datetime.utcnow().isoformat()

        c.execute("""
            INSERT INTO attendance (student_id, name, timestamp)
            VALUES (?, ?, ?)
        """, (student_id, name, ts))

        conn.commit()

    conn.close()