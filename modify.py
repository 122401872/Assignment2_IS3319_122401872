import sqlite3

db_name = "WorldGaming.db"

# Connect to the database
connection = sqlite3.connect(db_name)
cursor = connection.cursor()

# Add the 'console' column if it doesn't exist
try:
    cursor.execute("ALTER TABLE products ADD COLUMN console TEXT")
    print("Column 'console' added successfully.")
except sqlite3.OperationalError:
    print("Column 'console' already exists.")

# Commit changes and close the connection
connection.commit()
connection.close()
