"""
INF1103 Week 10 - Inventory class
Aggregation: an Inventory contains Product objects, but it does NOT create them
and does NOT control their lifecycle. A Product can exist before it is added,
be removed, and be added to a different Inventory.
Responsibility: manage a COLLECTION of Product objects.
"""
from product import Product


class Inventory:
    def __init__(self) -> None:
        # Typed with the base class so ANY kind of Product can be stored (LSP)
        self.__products: list[Product] = []

    @property
    def products(self) -> tuple[Product, ...]:
        """Read-only view so callers can loop: for product in inventory.products"""
        return tuple(self.__products)

    def add_product(self, product: Product) -> bool:
        if self.find_product(product.get_product_id()) is not None:
            return False

        self.__products.append(product)
        return True

    def remove_product(self, product_id: str) -> bool:
        # Only the REFERENCE is removed. The Product object itself is not destroyed.
        product: Product | None = self.find_product(product_id)
        if product is None:
            return False

        self.__products.remove(product)
        return True

    def find_product(self, product_id: str) -> Product | None:
        for product in self.__products:
            if product.get_product_id() == product_id:
                return product
        return None

    def get_all_products(self) -> tuple[Product, ...]:
        return tuple(self.__products)

    def display_all(self) -> None:
        print("Current Inventory")
        print("-" * 48)
        if len(self.__products) == 0:
            print("No products in inventory.")
        for product in self.__products:
            product.display_information()
        print("-" * 48)
