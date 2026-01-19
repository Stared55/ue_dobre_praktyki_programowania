# tasks.py
from celery import Celery
import numpy as np
import cv2
import base64
import os
import sys
import json
import redis
from datetime import datetime

# Fix import path
sys.path.append(os.getcwd())
from core import ANPR

# 1. Setup Celery
celery_app = Celery(
    "anpr_worker",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

# 2. Setup Redis for History Storage
# We use a separate connection to push successful results to a list
redis_client = redis.Redis(host='localhost', port=6379, db=0)

# 3. Load Model (Global)
print("Initializing Worker Model...")
anpr_service = ANPR(model_path="best.pt")

@celery_app.task(name="process_plate_task")
def process_plate_task(image_b64: str, filename: str):
    """
    Processes image and saves result to history.
    """
    try:
        # Decode
        img_bytes = base64.b64decode(image_b64)
        nparr = np.frombuffer(img_bytes, np.uint8)
        im0 = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Inference
        results = anpr_service.process_image_array(im0)

        # --- SAVE TO HISTORY ---
        # Create a record with timestamp
        history_record = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "filename": filename,
            "detections": results
        }
        
        # Push to the head of the list "anpr_history"
        # json.dumps converts dict to string
        redis_client.lpush("anpr_history", json.dumps(history_record))

        return results

    except Exception as e:
        return {"error": str(e)}