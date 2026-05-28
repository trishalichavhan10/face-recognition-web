import cv2
from model import extract_embedding_for_image

img = cv2.imread("test.jpg")
emb = extract_embedding_for_image(img)
if emb is not None:
    print("Extracted successfully!")
else:
    print("Failed to extract embedding!")
