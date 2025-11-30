import csv
import os
import uuid

from main import FILE_NAME

def add_task(description):
    file_exists = os.path.isfile(FILE_NAME)
    
    with open(FILE_NAME, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['id', 'status', 'description'])
        task_id = str(uuid.uuid4())
        writer.writerow([task_id, 'pending', description])
        print(f"Added task: {task_id} - {description}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python3 producer.py 'Task description'")
    else:
        task_desc = sys.argv[1]
        add_task(task_desc)