# main.py
from fastapi import FastAPI, UploadFile, File, HTTPException
from celery.result import AsyncResult
from tasks import celery_app, process_plate_task
import base64
import redis
import json

app = FastAPI()

# Connect to Redis to read the history list
redis_client = redis.Redis(host='localhost', port=6379, db=0)

@app.post("/detect-plate")
async def detect_plate(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image.")

    contents = await file.read()
    image_b64 = base64.b64encode(contents).decode("utf-8")

    # Pass 'file.filename' to the task now
    task = process_plate_task.delay(image_b64, file.filename)

    return {
        "task_id": task.id,
        "status": "queued",
        "check_result": f"/result/{task.id}"
    }

@app.get("/result/{task_id}")
async def get_result(task_id: str):
    task_result = AsyncResult(task_id, app=celery_app)
    if task_result.state == 'SUCCESS':
        return {"status": "completed", "result": task_result.result}
    elif task_result.state == 'FAILURE':
        return {"status": "failed", "error": str(task_result.result)}
    return {"status": task_result.state}

# --- NEW ENDPOINT ---
@app.get("/history")
async def get_history():
    """
    Fetch all processed results from Redis history.
    """
    # lrange(key, start, end) -> 0, -1 means "get everything"
    raw_history = redis_client.lrange("anpr_history", 0, -1)
    
    # Redis returns bytes, so we must decode and load JSON
    parsed_history = []
    for item in raw_history:
        try:
            parsed_history.append(json.loads(item))
        except:
            continue
            
    return parsed_history

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)