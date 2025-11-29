import csv
import os
from models.movie_models import Movie

def read_csv_to_objects(csv_file_path: str, model_class):
    if not os.path.exists(csv_file_path):
        return {"error": f"File '{csv_file_path}' not found."}

    objects = []
    with open(csv_file_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Tworzymy obiekt modelu, przekazując wartości z wiersza CSV
            obj = model_class(**row)
            objects.append(obj)
            
    return objects