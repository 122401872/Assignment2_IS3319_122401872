from dao.ProductDAO import ProductDAO

class ProductService:
    def __init__(self, db_name="WorldGaming.db"):
        self.productDAO = ProductDAO(db_name=db_name)

    def get_all_products(self):
        """Retrieve all products from the database."""
        return self.productDAO.get_all_products()

    def get_product_details(self, product_id):
        """Retrieve details of a product by its ID."""
        return self.productDAO.get_product_by_id(product_id)

    def get_products_by_console(self, console):
        """Retrieve products filtered by console."""
        return self.productDAO.get_products_by_console(console)
