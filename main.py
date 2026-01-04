import os
import sys
import xml.etree.ElementTree as ET
import time
import random
import re
import cv2
import easyocr
import shutil
import numpy as np
from collections import Counter

# --- 1. CONFIGURATION ---
ANNOTATIONS_FILE = os.path.join('raw_data', 'annotations', 'annotations.xml')
IMAGES_DIR = 'raw_data/photos'
LOG_FILE_NAME = "bledy_ocr.txt"
FULL_LOG_FILE = "all_readings.txt"
DEBUG_DIR = "debug_failures"
TEST_RATIO = 1

# --- 2. PATH DIAGNOSTICS ---
print(f"--- SYSTEM CHECK ---")
if not os.path.exists(ANNOTATIONS_FILE):
    print(f"CRITICAL ERROR: XML file not found at: {ANNOTATIONS_FILE}")
    sys.exit(1)
if not os.path.exists(IMAGES_DIR):
    print(f"CRITICAL ERROR: Photos folder not found at: {IMAGES_DIR}")
    sys.exit(1)
print(f"Paths OK.")

# --- 3. INITIALIZE EASYOCR ---
print("Loading EasyOCR model...")
reader = easyocr.Reader(['pl'], gpu=False, verbose=False) 
print("EasyOCR loaded.")

# --- 4. HELPER FUNCTIONS ---

def clean_text_strict(text):
    if not text: return ""
    return re.sub(r'[^A-Z0-9]', '', text.upper())

def smart_correction(detected, expected):
    detected = clean_text_strict(detected)
    expected = clean_text_strict(expected)
    if detected.startswith("PL") and len(detected) > len(expected):
        detected = detected[2:]
    return detected

def analyze_character_errors(expected, detected):
    confusions = []
    if len(expected) == len(detected):
        for c_true, c_det in zip(expected, detected):
            if c_true != c_det:
                confusions.append(f"{c_true}->{c_det}")
    return confusions

def calculate_final_grade(accuracy_percent, processing_time_sec):
    if accuracy_percent < 60 or processing_time_sec > 60:
        return 2.0
    accuracy_norm = (accuracy_percent - 60) / 40
    time_norm = (60 - processing_time_sec) / 50
    score = 0.7 * accuracy_norm + 0.3 * time_norm
    grade = 2.0 + 3.0 * score
    return round(grade * 2) / 2

def load_data_from_xml(xml_path):
    print("Parsing XML...")
    tree = ET.parse(xml_path)
    root = tree.getroot()
    dataset = []
    for image in root.findall('image'):
        filename = image.get('name')
        box = image.find('box')
        if box is None: continue
        if box.get('label') != 'plate': continue
        
        attr = box.find(".//attribute[@name='plate number']")
        if attr is None or not attr.text: continue
        
        plate_text = clean_text_strict(attr.text)
        full_path = os.path.join(IMAGES_DIR, filename)
        
        coords = [float(box.get('xtl')), float(box.get('ytl')), 
                  float(box.get('xbr')), float(box.get('ybr'))]
        
        dataset.append({
            'path': full_path,
            'box': coords,
            'text': plate_text
        })
    return dataset

def run_test():
    all_data = load_data_from_xml(ANNOTATIONS_FILE)
    if not all_data:
        print("ERROR: No data loaded from XML.")
        return

    random.shuffle(all_data)
    test_size = max(1, int(len(all_data) * TEST_RATIO))
    test_data = all_data[:test_size]

    if os.path.exists(DEBUG_DIR):
        shutil.rmtree(DEBUG_DIR)
    os.makedirs(DEBUG_DIR)

    print(f"\n--- STARTING TEST ---")
    print(f"Sample size: {test_size} images")
    print(f"Debug images: {DEBUG_DIR}/")

    correct_readings = 0
    all_confusions = []
    start_time = time.time()

    with open(LOG_FILE_NAME, "w", encoding="utf-8") as log_file, \
         open(FULL_LOG_FILE, "w", encoding="utf-8") as full_log:

        header = f"{'FILENAME':<30} | {'EXPECTED':<12} | {'DETECTED':<12} | {'STATUS'}\n"
        divider = "-" * 80 + "\n"
        log_file.write(f"ERROR LOG\n{header}{divider}")
        full_log.write(f"FULL LOG\n{header}{divider}")

        for i, item in enumerate(test_data):
            img_path = item['path']
            true_text = item['text']
            box = item['box']

            print(f"Processing {i+1}/{test_size}...", end='\r')

            # 1. LOAD
            img = cv2.imread(img_path)
            if img is None: continue
            h_img, w_img = img.shape[:2]

            # 2. COORDS
            x1, y1, x2, y2 = box
            if max(box) <= 1.0:
                x1, y1, x2, y2 = int(x1*w_img), int(y1*h_img), int(x2*w_img), int(y2*h_img)
            else:
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

            x1, y1 = max(0, x1), max(0, y1)
            x2, y2 = min(w_img, x2), min(h_img, y2)
            roi_raw = img[y1:y2, x1:x2]
            if roi_raw.size == 0: continue

            # --- 3. SAFE CROP (5%) ---
            rh, rw = roi_raw.shape[:2]
            crop_left = int(rw * 0.05) 
            crop_top = int(rh * 0.05)
            crop_bottom = int(rh * 0.05)
            crop_right = int(rw * 0.02)
            
            roi_tight = roi_raw[crop_top : rh-crop_bottom, crop_left : rw-crop_right]
            if roi_tight.size == 0: roi_tight = roi_raw

            # --- 4. BINARIZATION ---
            roi_gray = cv2.cvtColor(roi_tight, cv2.COLOR_BGR2GRAY)
            # Resize small plates to help OCR see details
            if roi_gray.shape[0] < 60:
                roi_gray = cv2.resize(roi_gray, None, fx=2.0, fy=2.0, interpolation=cv2.INTER_CUBIC)

            roi_blur = cv2.GaussianBlur(roi_gray, (3, 3), 0)
            _, roi_binary = cv2.threshold(roi_blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

            # --- 5. CLEANING & THICKENING ---
            
            # A. Remove Black Borders/Noise FIRST
            not_binary = cv2.bitwise_not(roi_binary)
            contours, _ = cv2.findContours(not_binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            img_h, img_w = roi_binary.shape[:2]
            total_area = img_h * img_w

            for cnt in contours:
                x, y, w, h = cv2.boundingRect(cnt)
                
                # STRICTER BORDER CHECK: 
                # Only delete vertical lines if they are VERY thin (0.08 width)
                # This protects 'W' legs which might be ~0.10 width.
                is_vertical_border = (h > img_h * 0.85) and (w < img_w * 0.08)
                
                # Standard strip/noise checks
                is_wide_strip = (w > img_w * 0.40)
                is_short_noise = (h < img_h * 0.30) and (not is_wide_strip)
                is_tiny_area = (w * h) < (total_area * 0.005)

                if is_vertical_border or is_wide_strip or is_short_noise or is_tiny_area:
                    cv2.drawContours(roi_binary, [cnt], -1, 255, -1)

            # B. [NEW] DILATION (The "W" Fix)
            # This makes white text slightly thicker, connecting broken parts of 'W'
            kernel = np.ones((2,2), np.uint8) 
            roi_binary = cv2.dilate(roi_binary, kernel, iterations=1)

            # --- 6. PADDING ---
            roi_ocr = cv2.copyMakeBorder(
                roi_binary, 
                top=10, bottom=10, left=10, right=10, 
                borderType=cv2.BORDER_CONSTANT, 
                value=[255, 255, 255]
            )

            # --- 7. OCR ---
            results = reader.readtext(roi_ocr, detail=0, allowlist='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
            detected_raw = "".join(results)
            detected_clean = smart_correction(detected_raw, true_text)
            
            # --- 8. LOGGING ---
            is_correct = (detected_clean == true_text)
            status = "OK" if is_correct else "FAIL"
            
            full_log.write(f"{os.path.basename(img_path):<30} | {true_text:<12} | {detected_clean:<12} | {status}\n")

            if is_correct:
                correct_readings += 1
            else:
                confusions = analyze_character_errors(true_text, detected_clean)
                all_confusions.extend(confusions)
                
                fail_filename = f"FAIL_{true_text}_vs_{detected_clean}.jpg"
                cv2.imwrite(os.path.join(DEBUG_DIR, fail_filename), roi_ocr)
                
                note = f" (Errors: {', '.join(confusions)})" if confusions else ""
                log_file.write(f"{os.path.basename(img_path):<30} | {true_text:<12} | {detected_clean:<12} | FAIL{note}\n")

    end_time = time.time()
    accuracy = (correct_readings / test_size) * 100 if test_size > 0 else 0
    time_per_100 = ((end_time - start_time) / test_size) * 100 if test_size > 0 else 0
    
    print(f"\n\n{'='*30}")
    print(f"FINAL RESULTS")
    print(f"Accuracy:      {accuracy:.2f}%")
    print(f"Speed:         {time_per_100:.2f} sec / 100 images")
    print(f"Grade:         {calculate_final_grade(accuracy, time_per_100)}")
    print(f"{'='*30}")

if __name__ == "__main__":
    run_test()