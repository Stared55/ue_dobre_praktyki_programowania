import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

movie_file_path = os.path.join(BASE_DIR, "database", "movies.csv")
link_file_path = os.path.join(BASE_DIR, "database", "links.csv")
tag_file_path = os.path.join(BASE_DIR, "database", "tags.csv")
rating_file_path = os.path.join(BASE_DIR, "database", "ratings.csv")

# loaders/loader_routes.py

import csv
from fastapi import APIRouter
from utils.session import SessionLocal

from models.movie_models import Movie
from models.link_models import Link
from models.tag_models import Tag
from models.rating_models import Rating

router = APIRouter(prefix="/load-csv", tags=["CSV Loaders"])


def bulk_import(model, file_path):
    db = SessionLocal()
    try:
        with open(file_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            items = [model(**row) for row in reader]

        db.bulk_save_objects(items)
        db.commit()
        return {"status": "loaded", "rows": len(items)}

    except Exception as e:
        db.rollback()
        return {"error": str(e)}

    finally:
        db.close()


@router.post("/movies")
def load_movies():
    return bulk_import(Movie, movie_file_path)


@router.post("/links")
def load_links():
    return bulk_import(Link, link_file_path)


@router.post("/tags")
def load_tags():
    return bulk_import(Tag, tag_file_path)


@router.post("/ratings")
def load_ratings():
    return bulk_import(Rating, rating_file_path)