import logging
import uuid
import requests
import numpy as np
import cv2 as cv

from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from consumer import test

# -----------------------------------------------------------------------------
# LOGGING
# -----------------------------------------------------------------------------

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("api")

# -----------------------------------------------------------------------------
# FASTAPI LIFESPAN
# -----------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 FastAPI server is starting... see: http://127.0.0.1:8000/docs")
    yield
    logger.info("🛑 FastAPI server is shutting down...")

# -----------------------------------------------------------------------------
# FASTAPI APP
# -----------------------------------------------------------------------------

app = FastAPI(
    title="Dobre Praktyki Programowania API",
    description="developed by Radosław Staroszyński",
    version="1.0.0",
    lifespan=lifespan,
)

# -----------------------------------------------------------------------------
# IMAGE LOADER
# -----------------------------------------------------------------------------

def load_image_from_url(url: str) -> np.ndarray:
    response = requests.get(url, timeout=10)

    logger.info(f"Downloading image: {url}")
    logger.info(f"HTTP status: {response.status_code}")

    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Image download failed")

    image_data = np.asarray(bytearray(response.content), dtype=np.uint8)
    img = cv.imdecode(image_data, cv.IMREAD_COLOR)

    if img is None:
        raise HTTPException(status_code=400, detail="Invalid image format")

    return test()

# -----------------------------------------------------------------------------
# API ENDPOINT
# -----------------------------------------------------------------------------

@app.get("/analyze_img/")
async def analyze_img(image_url: str):
    logger.info(f"Received request to analyze image: {image_url}")

    job_id = str(uuid.uuid4())

    # Load image (this validates the URL and image)
    img = load_image_from_url(image_url)

    # At this point the image is successfully loaded
    logger.info(f"Image loaded successfully for job {job_id}")

    return {
        "status": "queued",
        "job_id": job_id,
        "image_url": image_url,
    }