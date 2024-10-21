from typing import Dict, Any
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends
import duckdb
from pydantic import BaseModel


DATABASE_FILE = "app/data/budget_buddy.db"


@asynccontextmanager
async def lifespan(app: FastAPI):
    conn = duckdb.connect(DATABASE_FILE)
    conn.execute(
        """
    CREATE TABLE IF NOT EXISTS transaction (
                 id INTEGER PRIMARY KEY,
                 card TEXT,
                 posting_date DATE,
                 description TEXT,
                 amount DECIMAL(10, 2),
                 type TEXT,
                 category TEXT,
                 balance DECIMAL(10, 2), 
                 )
                 """
    )
    conn.close()

    yield


app = FastAPI(lifespan=lifespan)


def get_db():
    conn = duckdb.connect(DATABASE_FILE)
    try:
        yield conn
    finally:
        conn.close()


class Transaction(BaseModel):
    name: str


@app.on_event("startup")
async def startup():
    conn = duckdb.connect(DATABASE_FILE)
    conn.execute(
        """
    CREATE TABLE IF NOT EXISTS transaction (
                 id INTEGER PRIMARY KEY,
                 card TEXT,
                 posting_date DATE,
                 description TEXT,
                 amount DECIMAL(10, 2),
                 type TEXT,
                 category TEXT,
                 balance DECIMAL(10, 2), 
                 )
                 """
    )


@app.post("/transactions")
async def get_transactions(conn=Depends(get_db)) -> Dict[str, Any]:
    """
    Get all transactions
    """
    conn = duckdb.connect(DATABASE_FILE)
    result = conn.execute("SELECT * FROM transactions").fetchall()
    return {"transactions": result}
