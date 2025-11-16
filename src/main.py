import os
from fastapi import FastAPI
from models import Movie, Link, Rating, Tag
from utils.csv_reader import read_csv_to_objects

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MOVIES_CSV = os.path.join(BASE_DIR, "src/database", "movies.csv")
LINKS_CSV = os.path.join(BASE_DIR, "src/database", "links.csv")
RATINGS_CSV = os.path.join(BASE_DIR, "src/database", "ratings.csv")
TAGS_CSV = os.path.join(BASE_DIR, "src/database", "tags.csv")

@app.get("/")
def read_root():
    return {"message": "Hello, world!"}

@app.get("/movies")
def get_movies():
    movies = read_csv_to_objects(MOVIES_CSV, Movie)
    if isinstance(movies, dict) and "error" in movies:
        return movies
    return [m.__dict__ for m in movies]

@app.get("/links")
def get_links():
    links = read_csv_to_objects(LINKS_CSV, Link)
    if isinstance(links, dict) and "error" in links:
        return links
    return [l.__dict__ for l in links]

@app.get("/ratings")
def get_ratings():
    ratings = read_csv_to_objects(RATINGS_CSV, Rating)
    if isinstance(ratings, dict) and "error" in ratings:
        return ratings
    return [r.__dict__ for r in ratings]

@app.get("/tags")
def get_tags():
    tags = read_csv_to_objects(TAGS_CSV, Tag)
    if isinstance(tags, dict) and "error" in tags:
        return tags
    return [t.__dict__ for t in tags]