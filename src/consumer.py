import csv
import time
import os

from main import FILE_NAME, CHECK_INTERVAL, TASK_DURATION

def read_tasks():
    if not os.path.isfile(FILE_NAME):
        return []
    with open(FILE_NAME, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return list(reader)

def write_tasks(tasks):
    with open(FILE_NAME, mode='w', newline='', encoding='utf-8') as file:
        fieldnames = ['id', 'status', 'description']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(tasks)

def consume_task():
    tasks = read_tasks()
    for task in tasks:
        if task['status'] == 'pending':
            print(f"Consuming task {task['id']}: {task['description']}")
            task['status'] = 'in_progress'
            write_tasks(tasks)

            time.sleep(TASK_DURATION)

            task['status'] = 'done'
            write_tasks(tasks)
            print(f"Task {task['id']} done.")
            return True
    return False

if __name__ == "__main__":
    print("Consumer running...")
    while True:
        task_found = consume_task()
        if not task_found:
            time.sleep(CHECK_INTERVAL)