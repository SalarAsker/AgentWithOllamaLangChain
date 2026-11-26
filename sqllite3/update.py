import sqlite3



try:
    with sqlite3.connect("shop.db") as conn:
        cursor = conn.cursor()

        # SQL command to update a student's age
        update_query = '''
        UPDATE products 
        SET name = ? 
        WHERE product_id = ?;
        '''
        # Data for the update
        name = "laptop 5g"
        id = 1

        # Execute the SQL command with the data
        cursor.execute(update_query, (name, id))
    
except sqlite3.OperationalError as e:
    print("Failed to open database:", e)
