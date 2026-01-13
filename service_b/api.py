import pika
import json
import uuid
import os
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Service B - AI Producer")

RABBIT_HOST = os.getenv("RABBITMQ_HOST", "localhost")

class ImageRequest(BaseModel):
    url: str

def get_channel():
    connection = pika.BlockingConnection(pika.ConnectionParameters(RABBIT_HOST))
    return connection, connection.channel()

@app.post("/analyze_img/")
async def analyze_img(req: ImageRequest):
    job_id = str(uuid.uuid4())
    
    connection, channel = get_channel()
    channel.queue_declare(queue='ai_tasks', durable=True)
    
    message = json.dumps({"job_id": job_id, "url": req.url})
    
    channel.basic_publish(
        exchange='',
        routing_key='ai_tasks',
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent
        ))
    
    connection.close()
    return {"job_id": job_id, "status": "queued"}