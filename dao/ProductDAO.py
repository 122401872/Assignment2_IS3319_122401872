import sqlite3
from Classes.Product import Product

class ProductDAO:
    def __init__(self, db_name="WorldGaming.db"):
        self.db_name = db_name
        self._initialize_database()

    def _initialize_database(self):
        """Initializes the database and creates the products table if it doesn't exist."""
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()

        # Creates table if it does not exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                product_id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                product_image_name TEXT NOT NULL,
                price TEXT NOT NULL,
                unique_attributes TEXT NOT NULL
            )
        ''')

        # Checks if 'console' column exists before adding it
        cursor.execute("PRAGMA table_info(products)")
        columns = [row[1] for row in cursor.fetchall()]

        if "console" not in columns:
            cursor.execute("ALTER TABLE products ADD COLUMN console TEXT")  # No NOT NULL

        connection.commit()
        connection.close()

        self._populate_initial_data()

    def _populate_initial_data(self):
        """Populates the database with initial product data if the table is empty."""
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()

        # Checks if the table is empty
        cursor.execute("SELECT COUNT(*) FROM products")
        if cursor.fetchone()[0] == 0:
            initial_products = [
                (1, 'Xbox Controller', 'The Xbox One Controller is designed for ultimate precision and comfort during gaming sessions. With its ergonomic shape, responsive buttons, and textured grip, it offers superior control for an enhanced gaming experience. Featuring wireless connectivity, this controller ensures smooth, lag-free performance, whether you are playing on your Xbox One console or PC. The updated thumbsticks and D-pad provide improved accuracy, while the integrated 3.5mm headset jack allows for seamless audio communication. Compatible with a wide range of Xbox One games, it’s a must-have accessory for any serious gamer. Available in multiple colors to match your style', '/images/Xbox1.webp', '€60', 'Xbox Console Compatible, AA batteries, regular triggers', 'Xbox'),
                (2, 'Playstation 4 Controller', 'The PlayStation 4 DualShock 4 Wireless Controller is designed to redefine your gaming experience with intuitive controls and innovative features. Its ergonomic design ensures hours of comfortable gameplay, while the enhanced analog sticks and trigger buttons provide unmatched precision and responsiveness.', 'images/Playstation4.webp', '€40', 'Playstation 4 Console Compatible, Built-in Batteries, Regular triggers', 'Playstation'),
                (3, 'Playstation 5 Controller', 'Elevate your gaming experience with the PlayStation 5 DualSense Wireless Controller, a revolutionary design combining immersive features with unmatched precision.', '/images/Playstation5.webp', '€80', 'Playstation 5 Console Compatible, Built-in Batteries, Dynamic Adaptive Triggers', 'Playstation'),
                (4, 'Xbox Wired Controller', 'Elevate your gaming experience with the Xbox Wired Controller, a perfect combination of comfort, precision, and reliability. Designed for Xbox Series X|S, Xbox One, and Windows PCs, this controller ensures seamless compatibility and effortless connectivity', '/images/Xbox_Budget.webp', '€30', 'Xbox Console Compatible, AA batteries, regular triggers', 'Xbox'),
                (5, 'Nintendo Switch Controller', 'Elevate your gaming experience with the Nintendo Switch Controller, designed for precision, comfort, and seamless gameplay. Whether you’re exploring vast open worlds or competing in high-stakes battles, this controller offers the versatility you need.', '/images/Nintendo.webp', '€59.99', 'Nintendo Switch Console Compatible, Built-in, regular triggers', 'Nintendo')
            ]
            cursor.executemany('''
                INSERT INTO products (product_id, title, description, product_image_name, price, unique_attributes, console)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', initial_products)

        connection.commit()
        connection.close()

    def get_all_products(self):
        """Returns a list of all products."""
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM products")
        rows = cursor.fetchall()
        connection.close()

        products = [
            Product(product_id=row[0], title=row[1], description=row[2], product_image_name=row[3], price=row[4], unique_attributes=row[5].split(", "), console=row[6])
            for row in rows
        ]
        return products

    def get_product_by_id(self, product_id):
        """Returns a product by its ID or None if not found."""
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM products WHERE product_id = ?", (product_id,))
        row = cursor.fetchone()
        connection.close()

        if row:
            return Product(product_id=row[0], title=row[1], description=row[2], product_image_name=row[3], price=row[4], unique_attributes=row[5].split(", "), console=row[6])
        return None

    def get_all_consoles(self):
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute("SELECT DISTINCT console FROM products")
        rows = cursor.fetchall()
        connection.close()

        return [row[0] for row in rows]  # Return a list of console names

    def get_products_by_console(self, console):
        """Returns a list of products filtered by console."""
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM products WHERE console = ?", (console,))
        rows = cursor.fetchall()
        connection.close()

        return [
            Product(product_id=row[0], title=row[1], description=row[2], product_image_name=row[3], price=row[4],
                    unique_attributes=row[5].split(", "), console=row[6])
            for row in rows
        ]

    def delete_product_by_id(self, product_id):
        """Deletes a product by its ID."""
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute("DELETE FROM products WHERE product_id = ?", (product_id,))
        connection.commit()
        connection.close()


