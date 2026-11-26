

table_queries = {
    """
CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY, 
            name TEXT, 
            price REAL, 
            stock INTEGER);
""",
"""
CREATE TABLE IF NOT EXISTS customers (
            customer_id INTEGER PRIMARY KEY, 
            name TEXT, email TEXT, 
            account_status TEXT);
""",
"""
CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY, 
            customer_id INTEGER, 
            product_id INTEGER, 
            quantity INTEGER, 
            status TEXT);
""",
"""
CREATE TABLE IF NOT EXISTS deliveries (
            order_id INTEGER PRIMARY KEY, 
            carrier TEXT, 
            tracking_number TEXT, 
            status TEXT, 
            estimated_date TEXT);
""",
"""
CREATE TABLE IF NOT EXISTS payments (
            order_id INTEGER PRIMARY KEY, 
            method TEXT, 
            payment_status TEXT, 
            refund_status TEXT);
"""
}