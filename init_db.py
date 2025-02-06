from dao.ProductDAO import ProductDAO
from dao.UserDao import UserDAO
import sqlite3
import os

def initialize_database():
    # Initialize the ProductDAO, which creates the products table and populates initial data
    ProductDAO()
    print("Database initialized:'products' table created.")

    # Initialize the UserDAO, which creates the users table and populates initial data
    UserDAO()
    print("Database initialized: 'users' table created.")

def get_db_connection():
    conn = sqlite3.connect("WorldGaming.db")  # Make sure this is your correct database name
    conn.row_factory = sqlite3.Row  # This allows accessing columns by name instead of index
    return conn




if __name__ == "__main__":
    initialize_database()
