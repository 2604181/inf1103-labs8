"""
INF1103 Week 10 - PhysicalProduct
A PhysicalProduct IS-A Product, and it CAN be shipped (CanBeShipped).
"""
from product import Product
from can_be_shipped import CanBeShipped
from supplier import Supplier

# Simple shipping rule: flat fee + a charge per kilogram
SHIPPING_BASE_COST: float = 5.00
SHIPPING_COST_PER_KG: float = 2.00


class PhysicalProduct(Product, CanBeShipped):
    def __init__(self, product_id: str, name: str, price: float, stock: int,
                 supplier: Supplier, weight: float) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        if weight < 0:
            raise ValueError("Weight cannot be negative.")
        self.__weight: float = weight

    def get_weight(self) -> float:
        return self.__weight

    def display_information(self) -> None:
        super().display_information()
        print(f"    Type: Physical | Weight: {self.__weight:.2f} kg")

    def get_fulfilment_info(self) -> str:
        return "Requires physical shipping."

    def calculate_shipping_cost(self) -> float:
        return SHIPPING_BASE_COST + SHIPPING_COST_PER_KG * self.__weight
