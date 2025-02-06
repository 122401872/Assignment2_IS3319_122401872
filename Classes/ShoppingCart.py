from Classes import LineItem
from Converter.ConverToCurrency import convertNumberToPrice
class ShoppingCart:
    #holds a list of items in the shopping cart
    lineItems = []

    def __init__(self):
        self.lineItems = []

    def add_item(self, item: LineItem):
        self.lineItems.append(item)
    def delete_item(self, item: LineItem):
        self.lineItems.remove(item)

    def update_item(self, item: LineItem):
        for lineItem in self.lineItems:
            if lineItem.product.name == item.product.name:
                lineItem.itemQuantity += item.itemQuantity

    def cartTotal(self):
        cartPrice = 0.0
        for lineItem in self.lineItems:

            cartPrice += lineItem.totalPrice

        return convertNumberToPrice(cartPrice)