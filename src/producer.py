import sqlite3
import uuid
import sys

DB = "queue.db"

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

def add_task(description):
    conn = sqlite3.connect(DB)
    task_id = str(uuid.uuid4())
    conn.execute(
        "INSERT INTO tasks (id, status, description) VALUES (?, ?, ?)",
        (task_id, "pending", description)
    )
    conn.commit()
    conn.close()
    print(f"Task added: {task_id}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 producer.py \"Task description\"")
        sys.exit(1)

    init_db()
    add_task(sys.argv[1])