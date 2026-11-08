"""
INF1103 Week 8 - Inventory class
"""


class Inventory:
    def __init__(self):
        self.__products = []

    def add_product(self, product):
        if self.search_product(product.get_product_id()) is not None:
            return False

        self.__products.append(product)
        return True

    def search_product(self, product_id):
        for product in self.__products:
            if product.get_product_id() == product_id:
                return product
        return None

    def get_products(self):
        # Return a copy so outside code cannot change the internal list
        return list(self.__products)

    def display_all(self):
        print("Current Inventory")
        print("-" * 48)
        if len(self.__products) == 0:
            print("No products in inventory.")
        for product in self.__products:
            product.display_information()
        print("-" * 48)