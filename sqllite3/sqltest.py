import sqlite3

try:
    with sqlite3.connect("shop.db") as conn:
       cursor = conn.cursor()
       # Create products table command
       cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            price REAL NOT NULL,
            stock INTEGER NOT NULL DEFAULT 0
        )
"""         
       )
       print("Table product is created!")
except sqlite3.OperationalError as e:
    print("Failed to open database:", e)
