import sqlite3


def add_product(conn: sqlite3.Connection, product: list[tuple]) -> None:
        
    # Insert a record into the Students table
     insert_query = '''
            INSERT INTO products (name, price, stock) 
            VALUES (?, ?, ?);
            '''
     cursor = conn.cursor()
     cursor.executemany(insert_query, product)

try:
    with sqlite3.connect("shop.db") as conn:

     products = [
         ("graphics_card", 8500.0, 3),
         ("ram_kit", 1400.0, 9),
         ("router", 1250.0, 7),
         ("usb_hub", 290.0, 20),
            ]
     add_product(conn, products)
       
except sqlite3.OperationalError as e:
    print("Failed to open database:", e)
