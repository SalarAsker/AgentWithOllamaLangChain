import sqlite3

with sqlite3.connect("shop.db") as conn:
    # Create a cursor object
    cursor = conn.cursor()

    # Write the SQL command to select all records from the Students table
    select_query = "SELECT name, price FROM products WHERE name=?;"

    # Execute the SQL command
    cursor.execute(select_query,("laptop",))

    # Fetch all records
    record = cursor.fetchone()

    print(record)
   