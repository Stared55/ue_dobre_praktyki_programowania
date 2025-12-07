import sqlite3
import time

DB = "queue.db"
CHECK_INTERVAL = 5
TASK_DURATION = 30

def init_db():
    conn = sqlite3.connect(DB)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id TEXT PRIMARY KEY,
            status TEXT NOT NULL,
            description TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def acquire_task():
    conn = sqlite3.connect(DB)
    conn.isolation_level = None
    cursor = conn.cursor()

    cursor.execute("BEGIN IMMEDIATE")

    cursor.execute(
        "SELECT id, description FROM tasks WHERE status = 'pending' ORDER BY created_at LIMIT 1"
    )
    row = cursor.fetchone()

    if not row:
        conn.rollback()
        conn.close()
        return None

    task_id, desc = row

    cursor.execute(
        "UPDATE tasks SET status = 'in_progress' WHERE id = ?",
        (task_id,)
    )

    conn.commit()
    conn.close()
    return task_id, desc

def complete_task(task_id):
    conn = sqlite3.connect(DB)
    conn.execute(
        "UPDATE tasks SET status = 'done' WHERE id = ?",
        (task_id,)
    )
    conn.commit()
    conn.close()

def run():
    init_db()
    print("Consumer running...")
    while True:
        task = acquire_task()
        if not task:
            time.sleep(CHECK_INTERVAL)
            continue

        task_id, desc = task
        print(f"Processing: {task_id} - {desc}")

        time.sleep(TASK_DURATION)

        complete_task(task_id)
        print(f"Done: {task_id}")

if __name__ == "__main__":
    run()