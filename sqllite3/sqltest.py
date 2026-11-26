import sqlite3

# Create table queries
sql_statements = [ 
    """CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY, 
            name text NOT NULL, 
            begin_date DATE, 
            end_date DATE
        );""",

    """CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY, 
            name TEXT NOT NULL, 
            priority INT, 
            project_id INT NOT NULL, 
            status_id INT NOT NULL, 
            begin_date DATE NOT NULL, 
            end_date DATE NOT NULL, 
            FOREIGN KEY (project_id) REFERENCES projects (id)
        );"""
]

try:
    with sqlite3.connect("shop.db") as conn:
       cursor = conn.cursor()
       
       # Create tables simultaneously
       for tab in sql_statements:
           cursor.execute(tab)
       
       print("Table product is created!")
except sqlite3.OperationalError as e:
    print("Failed to open database:", e)
