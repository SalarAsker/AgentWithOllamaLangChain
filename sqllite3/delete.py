import sqlite3

try:
    with sqlite3.connect("shop.db") as conn:
        cursor = conn.cursor()

            # SQL command to delete a student
        delete_query = '''
        DELETE FROM products 
        WHERE name = ?;
        '''
        # Data for the update
        name = "webcam"

        # Execute the SQL command with the data
        cursor.execute(delete_query, (name,))
    
except sqlite3.OperationalError as e:
    print("Failed to open database:", e)
