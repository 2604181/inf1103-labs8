"""
INF1103 Week 9 - File handling
Responsibility: load and save inventory data (JSON). No menus, no prompts.
Each saved product has a "type" ("physical" or "digital") so the correct
subclass can be recreated when loading.
"""
import json

from physical_product import PhysicalProduct
from digital_product import DigitalProduct

# Global Constant
INVENTORY_FILE = "inventory.json"


def product_from_dict(item):
    """Use the "type" identifier to create the correct Product subclass."""
    product_type = item["type"]

    if product_type == "physical":
        return PhysicalProduct(
            item["id"],
            item["name"],
            float(item["price"]),
            int(item["stock"]),
            float(item["weight"])
        )
    elif product_type == "digital":
        return DigitalProduct(
            item["id"],
            item["name"],
            float(item["price"]),
            int(item["stock"]),
            float(item["download_size"])
        )
    else:
        raise ValueError(f"Unknown product type: {product_type}")


def product_to_dict(product):
    """Turn a Product object into a dictionary that can be saved as JSON."""
    item = {
        "id": product.get_product_id(),
        "name": product.get_name(),
        "price": product.get_price(),
        "stock": product.get_stock()
    }

    if isinstance(product, PhysicalProduct):
        item["type"] = "physical"
        item["weight"] = product.get_weight()
    elif isinstance(product, DigitalProduct):
        item["type"] = "digital"
        item["download_size"] = product.get_download_size()
    else:
        raise ValueError("Unsupported product type.")

    return item


def load_inventory(filename=INVENTORY_FILE):
    products = []
    status = "not_found"

    try:
        with open(filename, "r") as file:
            data = json.load(file)

        if not isinstance(data, list):
            return [], "error"

        for item in data:
            products.append(product_from_dict(item))
        status = "loaded"

    except FileNotFoundError:
        products = []
        status = "not_found"
    except (json.JSONDecodeError, KeyError, TypeError, ValueError):
        products = []
        status = "error"

    return products, status


def save_inventory(products, filename=INVENTORY_FILE):
    data = []
    for product in products:
        data.append(product_to_dict(product))

    with open(filename, "w") as file:
        json.dump(data, file, indent=4)
