"""
INF1103 Week 9 - DigitalProduct
A DigitalProduct IS-A Product. It is NOT shipped, so it does not implement CanBeShipped.
"""

from product import Product


class DigitalProduct(Product):
    def __init__(self, product_id, name, price, stock, download_size):
        super().__init__(product_id, name, price, stock)
        if download_size < 0:
            raise ValueError("Download size cannot be negative.")
        self.__download_size = download_size

    def get_download_size(self):
        return self.__download_size

    def display_information(self):
        super().display_information()
        print(f"    Type: Digital | Download Size: {self.__download_size:.2f} MB")

    def get_fulfilment_info(self) -> str:
        return "Delivered digitally via download link."
