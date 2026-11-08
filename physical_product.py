"""
INF1103 Week 9 - PhysicalProduct
A PhysicalProduct IS-A Product, and it CAN be shipped (CanBeShipped).
"""

from can_be_shipped import CanBeShipped
from product import Product

# Simple shipping rule: flat fee + a charge per kilogram
SHIPPING_BASE_COST = 5.00
SHIPPING_COST_PER_KG = 2.00


class PhysicalProduct(Product, CanBeShipped):
    def __init__(self, product_id, name, price, stock, weight):
        super().__init__(product_id, name, price, stock)
        if weight < 0:
            raise ValueError("Weight cannot be negative.")
        self.__weight = weight

    def get_weight(self):
        return self.__weight

    def display_information(self):
        super().display_information()
        print(f"    Type: Physical | Weight: {self.__weight:.2f} kg")

    def get_fulfilment_info(self) -> str:
        return "Requires physical shipping."

    def calculate_shipping_cost(self) -> float:
        return SHIPPING_BASE_COST + SHIPPING_COST_PER_KG * self.__weight
