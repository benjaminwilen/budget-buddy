import duckdb

DATABASE_FILE = (
    "~/Users/benjaminwilen/budget-buddy/budget_buddy/backend/app/data/budget_buddy.db"
)


def get_db():
    conn = duckdb.connect(DATABASE_FILE)
    try:
        yield conn
    finally:
        conn.close()
