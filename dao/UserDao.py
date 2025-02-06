import sqlite3
from Classes.User import User

class UserDAO:
    def __init__(self, db_name="WorldGaming.db"):
        self.db_name = db_name
        self._initialize_database()

    def _initialize_database(self):
        """Initializes the database and creates the users table if it doesn't exist."""
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                userid INTEGER PRIMARY KEY,
                firstName TEXT NOT NULL,
                lastName TEXT NOT NULL,
                userEmail TEXT NOT NULL UNIQUE,
                userPassword TEXT NOT NULL,
                isAdmin BOOLEAN NOT NULL
            )
        ''')
        connection.commit()
        connection.close()
        self._populate_initial_data()

    def _populate_initial_data(self):
        """Populates the database with initial user data if the table is empty."""
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()

        # Check if the table is empty
        cursor.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] == 0:
            initial_users = [
                (1, 'John', 'Doe', 'john@gmail.com', 'pw1', 0),
                (2, 'Mary', 'Doe', 'mary@gmail.com', 'pw2', 1)
            ]
            cursor.executemany('''
                INSERT INTO users (userid, firstName, lastName, userEmail, userPassword, isAdmin)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', initial_users)

        connection.commit()
        connection.close()

    def get_all_users(self):
        """Returns a list of all users."""
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        connection.close()

        users = [
            User(userid=row[0], firstName=row[1], lastName=row[2], userEmail=row[3], userPassword=row[4], isAdmin=bool(row[5]))
            for row in rows
        ]
        return users

    def get_user_by_email(self, email):
        """Returns a user by their email or None if not found."""
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE userEmail = ?", (email,))
        row = cursor.fetchone()
        connection.close()

        if row:
            return User(userid=row[0], firstName=row[1], lastName=row[2], userEmail=row[3], userPassword=row[4], isAdmin=bool(row[5]))
        return None
