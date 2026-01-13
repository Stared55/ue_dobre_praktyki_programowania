import sqlite3

DB_NAME = "results.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS results (
            job_id TEXT PRIMARY KEY,
            status TEXT,
            person_count INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def update_job_status(job_id, status, count=None):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    if count is not None:
        cursor.execute("UPDATE results SET status = ?, person_count = ? WHERE job_id = ?", (status, count, job_id))
    else:
        cursor.execute("UPDATE results SET status = ? WHERE job_id = ?", (status, job_id))
    conn.commit()
    conn.close()

def create_job(job_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO results (job_id, status, person_count) VALUES (?, ?, ?)", (job_id, "queued", None))
    conn.commit()
    conn.close()

def get_job(job_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT status, person_count FROM results WHERE job_id = ?", (job_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {"status": row[0], "person_count": row[1]}
    return None