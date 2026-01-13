import logging
import uuid
import json
import pika
from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from database import init_db, create_job, get_job

# LOGGING
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("api")

# RABBITMQ CONNECTION
def get_rabbitmq_channel():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='image_queue')
    return connection, channel

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db() # Inicjalizacja bazy przy starcie
    logger.info("🚀 API starting...")
    yield
    logger.info("🛑 API shutting down...")

app = FastAPI(title="People Counter API", lifespan=lifespan)

# --- ENDPOINTS ---

@app.post("/analyze_img/")
async def analyze_img(image_url: str):
    job_id = str(uuid.uuid4())
    
    # 1. Zapisz wstępny status w bazie
    create_job(job_id)

    # 2. Wyślij zadanie do RabbitMQ
    try:
        connection, channel = get_rabbitmq_channel()
        message = json.dumps({"job_id": job_id, "url": image_url})
        
        channel.basic_publish(
            exchange='',
            routing_key='image_queue',
            body=message
        )
        connection.close()
    except Exception as e:
        logger.error(f"RabbitMQ Error: {e}")
        raise HTTPException(status_code=500, detail="Queue service unavailable")

    logger.info(f"Job {job_id} queued.")

    return {
        "status": "queued",
        "job_id": job_id,
        "info": "Use GET /result/{job_id} to check progress"
    }

@app.get("/result/{job_id}")
async def get_result(job_id: str):
    result = get_job(job_id)
    if not result:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return {
        "job_id": job_id,
        "status": result['status'],
        "people_detected": result['person_count']
    }