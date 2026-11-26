
import sqlite3
from config import SQL_DB_DIR
from langchain_core.tools import tool

path = SQL_DB_DIR / "nordictec.db"

#----------------------------
# # Helper function called by all the tools below
#----------------------------
def fetch_record(query, parameter):
    
    with sqlite3.connect(path) as conn:

        conn.row_factory = __import__('sqlite3').Row
        # execute the query
        row = conn.execute(query, (parameter,)).fetchone()
        
        return dict(row) if row else {'message': 'No matching record found.'}

#----------------------------
# Tools
#----------------------------
@tool
def get_order(order_id: int) -> dict:
    """Get an order's product, quantity, and status using its numeric order ID."""
    
    return fetch_record('''SELECT o.order_id, p.name AS product, o.quantity, o.status
                        FROM orders o JOIN products p ON p.product_id=o.product_id
                        WHERE o.order_id=?''', order_id)


@tool
def get_product(product_id: int) -> dict:
    """Get a product's name, price in SEK, and stock using its numeric product ID."""
    
    return fetch_record('SELECT * FROM products WHERE product_id=?', product_id)


@tool
def get_delivery(order_id: int) -> dict:
    """Get delivery carrier, tracking, status, and estimated date using an order ID."""
    
    return fetch_record('SELECT * FROM deliveries WHERE order_id=?', order_id)


@tool
def get_payment(order_id: int) -> dict:
    """Get payment method, payment status, and refund status using an order ID."""
    
    return fetch_record('SELECT * FROM payments WHERE order_id=?', order_id)


@tool
def get_account(customer_id: int) -> dict:
    """Get demo customer name, email, and account status using numeric customer ID."""
    
    return fetch_record('SELECT * FROM customers WHERE customer_id=?', customer_id)


if __name__ == "__main__":

    print(fetch_record('''SELECT o.order_id, p.name AS product, o.quantity, o.status
                        FROM orders o JOIN products p ON p.product_id=o.product_id
                        WHERE o.order_id=?''',1001))

    print(fetch_record('SELECT * FROM customers WHERE customer_id=?',2))