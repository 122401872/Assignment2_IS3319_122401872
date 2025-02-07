from Classes import LineItem, Product
from Converter.ConverToCurrency import convertNumberToPrice


class ShoppingCart:
    def __init__(self):
        self.lineItems = []

    def add_item(self, Product: LineItem):
        self.lineItems.append(Product)

    def delete_item(self, Product: LineItem):
        self.lineItems.remove(Product)

    def update_item(self, updated_product: LineItem):
        # Find the matching item by product name (or you could use an ID if available)
        for lineItem in self.lineItems:
            if lineItem.product.name == updated_product.product.name:
                # Update the quantity; totalPrice is automatically updated via the property.
                lineItem.itemQuantity = updated_product.itemQuantity
                break

    def cartTotal(self):
        # Calculate the cart total by summing the line item totals.
        cartPrice = sum(lineItem.totalPrice for lineItem in self.lineItems)
        return convertNumberToPrice(cartPrice)
