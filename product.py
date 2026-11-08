"""
INF1103 Week 9 - Product (abstract base class)
Responsibility: represent what is COMMON to every product and manage its own state.
"""
from abc import ABC, abstractmethod


class Product(ABC):
    def __init__(self, product_id, name, price, stock):
        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.__stock = stock

    def update_stock(self, quantity):
        # The Product decides how a new stock value is treated
        if quantity >= 0:
            self.__stock = quantity

    def get_product_id(self):
        return self.__product_id

    def get_name(self):
        return self.__name

    def get_price(self):
        return self.__price

    def get_stock(self):
        return self.__stock

    def display_information(self):
        print(
            f"ID: {self.__product_id} | Name: {self.__name} | "
            f"Price: ${self.__price:.2f} | Stock: {self.__stock}"
        )

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        """Return delivery/fulfilment information for this product type."""
