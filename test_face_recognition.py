import face_recognition
import cv2

image = face_recognition.load_image_file("test.jpg")
face_locations = face_recognition.face_locations(image)
print(f"I found {len(face_locations)} face(s) in this photograph.")
if len(face_locations) > 0:
    face_encodings = face_recognition.face_encodings(image, face_locations)
    print("Found encoding with shape:", face_encodings[0].shape)
