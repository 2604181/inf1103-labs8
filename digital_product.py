"""
INF1103 Week 10 - DigitalProduct
A DigitalProduct IS-A Product. It is NOT shipped, so it does not implement CanBeShipped.
"""
from product import Product
from supplier import Supplier


class DigitalProduct(Product):
    def __init__(self, product_id: str, name: str, price: float, stock: int,
                 supplier: Supplier, download_size: float) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        if download_size < 0:
            raise ValueError("Download size cannot be negative.")
        self.__download_size: float = download_size

    def get_download_size(self) -> float:
        return self.__download_size

    def display_information(self) -> None:
        super().display_information()
        print(f"    Type: Digital | Download Size: {self.__download_size:.2f} MB")

    def get_fulfilment_info(self) -> str:
        return "Delivered digitally via download link."
