import os
from fastapi import FastAPI
from routes.loaders import router as loader_router
from routes.movie_routes import router as movie_router
from routes.link_routes import router as link_router
from routes.tag_routes import router as tag_router
from routes.rating_routes import router as rating_router
from contextlib import asynccontextmanager
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(" ")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 FastAPI server is starting... see: http://127.0.0.1:8000/docs")
    yield
    logger.info("🛑 FastAPI server is shutting down...")

app = FastAPI(description="developed by stared55", title="Dobre Praktyki Programowania API", version="1.0.0", lifespan=lifespan)

app.include_router(movie_router)
app.include_router(link_router)
app.include_router(tag_router)
app.include_router(rating_router)
app.include_router(loader_router)