from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

app = FastAPI(title="Service A - Results Store")

DB_NAME = "storage.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS results (
            job_id TEXT PRIMARY KEY,
            count INTEGER,
            status TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

class ResultSchema(BaseModel):
    job_id: str
    count: int
    status: str

@app.post("/results/")
async def save_result(result: ResultSchema):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        # Upsert (insert or update)
        cursor.execute("""
            INSERT INTO results (job_id, count, status) VALUES (?, ?, ?)
            ON CONFLICT(job_id) DO UPDATE SET count=excluded.count, status=excluded.status
        """, (result.job_id, result.count, result.status))
        conn.commit()
        conn.close()
        return {"msg": "saved"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/results/{job_id}")
async def get_result(job_id: str):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT count, status FROM results WHERE job_id = ?", (job_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {"job_id": job_id, "count": row[0], "status": row[1]}
    raise HTTPException(status_code=404, detail="Not found")