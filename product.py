"""
INF1103 Week 10 - Product (abstract base class)
Responsibility: represent what is COMMON to every product and manage its own state.
Association: a Product refers to ONE Supplier (it does not own it).
"""
from abc import ABC, abstractmethod

from supplier import Supplier


class Product(ABC):
    def __init__(self, product_id: str, name: str, price: float,
                 stock: int, supplier: Supplier) -> None:
        self.__product_id: str = product_id
        self.__name: str = name
        self.__price: float = price
        self.__stock: int = stock
        self.__supplier: Supplier = supplier

    def update_stock(self, quantity: int) -> None:
        """
        Contract every Product (and every subclass) must keep:
        set the stock to `quantity` when quantity >= 0, ignore negative values,
        never raise an error, and return nothing.
        """
        if quantity >= 0:
            self.__stock = quantity

    def get_product_id(self) -> str:
        return self.__product_id

    def get_name(self) -> str:
        return self.__name

    def get_price(self) -> float:
        return self.__price

    def get_stock(self) -> int:
        return self.__stock

    def get_supplier(self) -> Supplier:
        return self.__supplier

    def display_information(self) -> None:
        print(
            f"ID: {self.__product_id} | Name: {self.__name} | "
            f"Price: ${self.__price:.2f} | Stock: {self.__stock}"
        )

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        """Return delivery/fulfilment information for this product type."""
