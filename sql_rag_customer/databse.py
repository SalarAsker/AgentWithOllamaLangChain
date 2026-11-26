import sqlite3
from config import SQL_DB_DIR
from create_table_queries import table_queries

# Ensure the sqldb_db directory exists before connecting
SQL_DB_DIR.mkdir(parents=True, exist_ok=True)
path = SQL_DB_DIR / "nordictec.db"

def create_table(conn:sqlite3.Connection):
    cursor = conn.cursor()
    
    for tab in table_queries:
        cursor.execute(tab)



try:
    with sqlite3.connect(path) as conn:
      create_table(conn)

except sqlite3.OperationalError as e:
    print("Failed to open database:", e)

