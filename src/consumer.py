import pika
import json
import cv2
import numpy as np
import requests
import logging
from database import update_job_status, init_db
from ultralytics import YOLO

# -----------------------------------------------------------------------------
# KONFIGURACJA I INICJALIZACJA MODELU
# -----------------------------------------------------------------------------
logging.basicConfig(level=logging.INFO, format='%(asctime)s - WORKER - %(message)s')
logger = logging.getLogger(__name__)

# Ładujemy model YOLOv8n (nano).
# Przy pierwszym uruchomieniu biblioteka sama pobierze plik "yolov8n.pt" (ok. 6MB).
model = YOLO("yolov8n.pt")

# -----------------------------------------------------------------------------
# LOGIKA DETEKCJI
# -----------------------------------------------------------------------------
def detect_people(image_url):
    try:
        logger.info(f"Downloading image from: {image_url}")
        resp = requests.get(image_url, timeout=10)
        
        if resp.status_code != 200:
            logger.error(f"Failed to download image: {resp.status_code}")
            return -1

        # Dekodowanie obrazu do formatu OpenCV
        image_data = np.asarray(bytearray(resp.content), dtype=np.uint8)
        img = cv2.imdecode(image_data, cv2.IMREAD_COLOR)

        if img is None:
            logger.error("Failed to decode image")
            return -1

        # --- DETEKCJA YOLO ---
        # conf=0.4 -> Pewność powyżej 40%
        # classes=[0] -> Szukaj tylko klasy '0' (w COCO dataset 0 to 'person')
        results = model.predict(img, conf=0.4, classes=[0], verbose=False)
        
        # results[0].boxes zawiera znalezione obiekty
        person_count = len(results[0].boxes)
        
        return person_count

    except Exception as e:
        logger.error(f"Error processing image: {e}")
        return -1

# -----------------------------------------------------------------------------
# OBSŁUGA RABBITMQ
# -----------------------------------------------------------------------------
def callback(ch, method, properties, body):
    try:
        data = json.loads(body)
        job_id = data.get('job_id')
        url = data.get('url')

        if not job_id or not url:
            logger.warning("Invalid message format received")
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return

        logger.info(f"Processing Job: {job_id}")
        update_job_status(job_id, "processing")

        count = detect_people(url)

        if count >= 0:
            update_job_status(job_id, "completed", count)
            logger.info(f"Job {job_id} success! People found: {count}")
        else:
            update_job_status(job_id, "failed", 0)
            logger.error(f"Job {job_id} failed.")

    except Exception as e:
        logger.error(f"Critical error in callback: {e}")
    finally:
        # Zawsze potwierdzamy odbiór, żeby nie blokować kolejki
        ch.basic_ack(delivery_tag=method.delivery_tag)

def start_worker():
    init_db()
    
    # Łączenie z RabbitMQ (z retry logic w produkcji, tu uproszczone)
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='image_queue')

        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue='image_queue', on_message_callback=callback)

        logger.info(' [*] Worker ready with YOLOv8. Waiting for messages...')
        channel.start_consuming()
    except Exception as e:
        logger.error(f"Could not connect to RabbitMQ: {e}")

if __name__ == "__main__":
    start_worker()