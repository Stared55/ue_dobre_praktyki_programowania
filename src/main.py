import os
from fastapi import FastAPI
from routes.loaders import router as loader_router
from routes.movie_routes import router as movie_router
from routes.link_routes import router as link_router
from routes.tag_routes import router as tag_router
from routes.rating_routes import router as rating_router

app = FastAPI()

app.include_router(movie_router)
app.include_router(link_router)
app.include_router(tag_router)
app.include_router(rating_router)
app.include_router(loader_router)