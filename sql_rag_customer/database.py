import sqlite3
from config import SQL_DB_DIR
from create_table_queries import table_queries

# Ensure the sqldb_db directory exists before connecting
SQL_DB_DIR.mkdir(parents=True, exist_ok=True)
path = SQL_DB_DIR / "nordictec.db"

#----------------------------
# Data
#----------------------------
# 1. products: (product_id, name, price, stock)
products = [
    (101, 'Wireless Mouse', 249, 20),
    (102, 'USB-C Hub', 399, 8),
    (103, 'Laptop Stand', 299, 0),
    (104, 'Mechanical Keyboard', 899, 14),
    (105, '4K Webcam', 1190, 5),
    (106, 'Noise-Cancelling Headset', 1490, 3),
]
# 2. customers: (customer_id, name, email, account_status)
customers = [
    (1, 'Alex Andersson', 'alex@example.com', 'active'),
    (2, 'Sam Nilsson', 'sam@example.com', 'active'),
    (3, 'Maja Lindqvist', 'maja@example.com', 'active'),
    (4, 'Erik Johansson', 'erik@example.com', 'suspended'),
]

# 3. orders: (order_id, customer_id, product_id, quantity, status)
orders = [
    (1001, 1, 101, 1, 'shipped'),
    (1002, 2, 102, 2, 'processing'),
    (1003, 1, 103, 1, 'cancelled'),
    (1004, 3, 104, 1, 'delivered'),
    (1005, 4, 105, 1, 'on hold'),
    (1006, 2, 106, 1, 'returned'),
]

# 4. deliveries: (order_id, carrier, tracking_number, status, estimated_date)
deliveries = [
    (1001, 'PostNord', 'DEMO-SE-1001', 'in transit', '2026-12-02'),
    (1002, 'PostNord', 'not assigned', 'not shipped', 'not available'),
    (1003, 'none', 'none', 'cancelled', 'not available'),
    (1004, 'DHL', 'DEMO-SE-1004', 'delivered', '2026-11-22'),
    (1005, 'Bring', 'not assigned', 'on hold', 'not available'),
    (1006, 'PostNord', 'DEMO-SE-1006', 'returned to sender', '2026-11-24'),
]

# 5. payments: (order_id, method, payment_status, refund_status)
payments = [
    (1001, 'card', 'paid', 'none'),
    (1002, 'Swish', 'paid', 'none'),
    (1003, 'card', 'refunded', 'completed'),
    (1004, 'Klarna', 'paid', 'none'),
    (1005, 'card', 'pending', 'none'),
    (1006, 'Swish', 'paid', 'in progress'),
]

# Function to create tables.
def create_table(conn:sqlite3.Connection):
    cursor = conn.cursor()
    
    for tab in table_queries:
        cursor.execute(tab)

# Database connection object.
try:
    with sqlite3.connect(path) as conn:
      
      # create tables
      create_table(conn)

      cursor = conn.cursor()
      # Insert into products table
      cursor.executemany('INSERT INTO products VALUES (?,?,?,?)', products)
      # Insert into customers table
      cursor.executemany('INSERT INTO customers VALUES (?,?,?,?)', customers)
      # Insert into orders table
      cursor.executemany('INSERT INTO orders VALUES (?,?,?,?,?)', orders)
      # Insert into deliveries table
      cursor.executemany('INSERT INTO deliveries VALUES (?,?,?,?,?)', deliveries)
            # Insert into payments table
      cursor.executemany('INSERT INTO payments VALUES (?,?,?,?)', payments)

except sqlite3.OperationalError as e:
    print("Failed to open database:", e)



