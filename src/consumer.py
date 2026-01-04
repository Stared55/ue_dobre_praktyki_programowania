import cv2

# Load the image
image_path = "src/example.jpg"
img = cv2.imread(image_path)

if img is None:
    print(f"Failed to load image at {image_path}")
    exit()

# Initialize HOG descriptor/person detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# Detect people in the image
(rects, weights) = hog.detectMultiScale(
    img,
    winStride=(4, 4),  # smaller step for better accuracy
    padding=(8, 8),
    scale=1.03  # smaller scale increment for multi-scale detection
)

# Filter overlapping boxes
from imutils.object_detection import non_max_suppression
import numpy as np

rects_np = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
pick = non_max_suppression(rects_np, probs=None, overlapThresh=0.65)

# Draw bounding boxes
for (xA, yA, xB, yB) in pick:
    cv2.rectangle(img, (xA, yA), (xB, yB), (0, 255, 0), 2)

# Display the result
cv2.imshow("Detected People", img)

while True:
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
cv2.waitKey(1)