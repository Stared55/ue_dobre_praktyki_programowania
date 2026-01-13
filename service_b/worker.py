import pika
import json
import os
import time
import requests
import logging
import cv2
import numpy as np
from ultralytics import YOLO

# Konfiguracja
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("worker")

RABBIT_HOST = os.getenv("RABBITMQ_HOST", "localhost")
SERVICE_A_URL = os.getenv("SERVICE_A_URL", "http://localhost:8001/results/")

# Model AI (ładowany raz przy starcie kontenera)
model = YOLO("yolov8n.pt")

def detect_people(url):
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code != 200:
            return None
        arr = np.asarray(bytearray(resp.content), dtype=np.uint8)
        img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        if img is None: return None
        
        results = model.predict(img, classes=[0], verbose=False) # 0 = person
        return len(results[0].boxes)
    except Exception as e:
        logger.error(f"AI Error: {e}")
        return None

def send_result_to_service_a(job_id, count, status="completed"):
    payload = {"job_id": job_id, "count": count, "status": status}
    try:
        response = requests.post(SERVICE_A_URL, json=payload, timeout=5)
        response.raise_for_status()
        return True
    except requests.RequestException as e:
        logger.error(f"Failed to connect to Service A: {e}")
        return False

def callback(ch, method, properties, body):
    data = json.loads(body)
    job_id = data['job_id']
    url = data['url']
    
    logger.info(f"Processing {job_id}...")

    # 1. Analiza obrazu
    count = detect_people(url)
    
    if count is None:
        # Błąd pobierania obrazu -> nie ma sensu ponawiać, oznaczamy jako błąd i wysyłamy do A
        # Jeśli A nie działa, to trudno, to zadanie i tak jest błędne.
        logger.error("Image failed.")
        send_result_to_service_a(job_id, 0, "failed")
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return

    # 2. Wysyłka wyniku do Serwisu A (RETRY STRATEGY)
    success = send_result_to_service_a(job_id, count)
    
    if success:
        logger.info(f"Job {job_id} sent to Service A. ACK.")
        ch.basic_ack(delivery_tag=method.delivery_tag)
    else:
        logger.warning(f"Service A unavailable. Requeuing job {job_id}...")
        time.sleep(2) # Krótka pauza, żeby nie ddosować własnego Rabbita
        # auto ack = false (w sensie nie wysyłamy ack, tylko nack z requeue)
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

def start():
    while True:
        try:
            params = pika.ConnectionParameters(RABBIT_HOST, heartbeat=600)
            connection = pika.BlockingConnection(params)
            channel = connection.channel()
            channel.queue_declare(queue='ai_tasks', durable=True)
            channel.basic_qos(prefetch_count=1)
            
            logger.info("Worker started. Waiting for messages...")
            channel.basic_consume(queue='ai_tasks', on_message_callback=callback)
            channel.start_consuming()
        except pika.exceptions.AMQPConnectionError:
            logger.info("Waiting for RabbitMQ...")
            time.sleep(5)

if __name__ == "__main__":
    start()