import sqlite3

name = input("Enter student name: ")

conn = sqlite3.connect("attendance.db")
cursor = conn.cursor()

cursor.execute("INSERT INTO students (name) VALUES (?)", (name,))
conn.commit()

print("Student added successfully!")

conn.close()