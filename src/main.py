import os
from fastapi import FastAPI
from models.movie_models import Movie
from utils.csv_reader import read_csv_to_objects

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MOVIES_CSV = os.path.join(BASE_DIR, "src/database", "movies.csv")

@app.get("/")
def read_root():
    return {"message": "Hello, world!"}

@app.get("/movies")
def get_movies():
    movies = read_csv_to_objects(MOVIES_CSV, Movie)
    if isinstance(movies, dict) and "error" in movies:
        return movies
    return [m.__dict__ for m in movies]
