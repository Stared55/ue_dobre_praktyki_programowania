# ======================================
# Ultralytics YOLO + EasyOCR
# Automatic Number Plate Recognition
# ======================================

import cv2
import torch
import easyocr
import numpy as np
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator, colors
import re


class ANPR:
    def __init__(self, model_path: str = "yolo11n.pt"):
        """Initializes the ANPR system."""
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = YOLO(model_path)
        self.reader = easyocr.Reader(["en"], gpu=torch.cuda.is_available())

    def detect_plates(self, im0: np.ndarray):
        """Detects license plates in a image."""
        results = self.model.predict(im0, verbose=False)
        boxes = results[0].boxes.xyxy.cpu().numpy() if results and results[0].boxes is not None else []
        return boxes

    def smart_correct_text(self, text: str):
        chars = list(text)
        length = len(chars)
        dict_char_to_int = {'O': '0', 'Q': '0', 'D': '0', 'I': '1', 'Z': '7', 'B': '8', 'G': '6', 'S': '5', 'A': '4'}
        dict_int_to_char = {'0': 'O', '1': 'I', '7': 'Z', '8': 'B', '6': 'G', '5': 'S', '4': 'A'}

        for i in range(length):
            char = chars[i]
            if i < 2: 
                if char in dict_int_to_char: chars[i] = dict_int_to_char[char]
            elif i >= 2:
                 if char in dict_char_to_int:
                    if char in ['O', 'Q', 'D']: chars[i] = '0'
                    if char == 'Z': chars[i] = '7'
        return "".join(chars)

    def extract_text(self, im0: np.ndarray, bbox: np.ndarray):
        x1, y1, x2, y2 = map(int, bbox)
        roi = im0[y1:y2, x1:x2]
        
        # Logic: Upscale -> Pad -> Thinning (Dilation) -> OCR
        scale = 2
        width = int(roi.shape[1] * scale)
        height = int(roi.shape[0] * scale)
        roi = cv2.resize(roi, (width, height), interpolation=cv2.INTER_CUBIC)
        roi = cv2.copyMakeBorder(roi, 15, 15, 15, 15, cv2.BORDER_CONSTANT, value=(255, 255, 255))
        
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        kernel = np.ones((2, 2), np.uint8)
        thinned = cv2.dilate(binary, kernel, iterations=1)

        results = self.reader.readtext(thinned, detail=1, batch_size=1)
        if not results: return ""

        parsed_results = [(box[2][1] - box[1][1], text) for box, text, conf in results]
        if not parsed_results: return ""

        max_height = max(h for h, t in parsed_results)
        filtered_text = [t for h, t in parsed_results if h >= max_height * 0.5]
        
        raw_text = "".join(filtered_text).strip()
        clean_text = re.sub(r'[^A-Z0-9]', '', raw_text.upper())
        return self.smart_correct_text(clean_text)


    def infer_image(self, image_path: str, display: bool = True):
        """Performs ANPR on a single image file."""
        # 1. Read the image
        im0 = cv2.imread(image_path)
        if im0 is None:
            print(f"Error: Could not read image at {image_path}")
            return

        # 2. Detect plates
        boxes = self.detect_plates(im0)
        
        # 3. Annotate and Extract Text
        ann = Annotator(im0, line_width=4)
        for bbox in boxes:
            text = self.extract_text(im0, bbox)
            print(f"Detected Plate: {text}") # Print text to console
            ann.box_label(bbox, label=text, color=colors(17, True))

        # 4. Display result
        if display:
            cv2.imshow("ANPR Result", im0)
            # waitKey(0) pauses the script indefinitely until a key is pressed
            cv2.waitKey(0) 
            cv2.destroyAllWindows()


if __name__ == "__main__":

    anpr = ANPR(model_path="best.pt")  # Use trained YOLO license plate model
    anpr.infer_image("raw_data/photos/82.jpg")
    # anpr.infer_image("raw_data/test.webp")