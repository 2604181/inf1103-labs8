"""
INF1103 Week 10 - File handling
Responsibility: load and save inventory data (JSON). No menus, no prompts.
Each saved product has a "type" ("physical" or "digital") and a "supplier".
Products with the same supplier id share ONE Supplier object when loaded.
"""
import json
from collections.abc import Sequence
from typing import Any

from product import Product
from supplier import Supplier
from physical_product import PhysicalProduct
from digital_product import DigitalProduct

# Global Constant
INVENTORY_FILE: str = "inventory.json"


def supplier_from_dict(data: dict[str, Any], suppliers: dict[str, Supplier]) -> Supplier:
    """Reuse an existing Supplier object if this supplier id was already loaded."""
    supplier_id: str = data["id"]
    if supplier_id not in suppliers:
        suppliers[supplier_id] = Supplier(supplier_id, data["name"], data["email"])
    return suppliers[supplier_id]


def product_from_dict(item: dict[str, Any], suppliers: dict[str, Supplier]) -> Product:
    """Use the "type" identifier to create the correct Product subclass."""
    supplier: Supplier = supplier_from_dict(item["supplier"], suppliers)
    product_type: str = item["type"]

    if product_type == "physical":
        return PhysicalProduct(
            item["id"],
            item["name"],
            float(item["price"]),
            int(item["stock"]),
            supplier,
            float(item["weight"])
        )
    elif product_type == "digital":
        return DigitalProduct(
            item["id"],
            item["name"],
            float(item["price"]),
            int(item["stock"]),
            supplier,
            float(item["download_size"])
        )
    else:
        raise ValueError(f"Unknown product type: {product_type}")


def product_to_dict(product: Product) -> dict[str, Any]:
    """Turn a Product object into a dictionary that can be saved as JSON."""
    supplier: Supplier = product.get_supplier()
    item: dict[str, Any] = {
        "id": product.get_product_id(),
        "name": product.get_name(),
        "price": product.get_price(),
        "stock": product.get_stock(),
        "supplier": {
            "id": supplier.get_supplier_id(),
            "name": supplier.get_name(),
            "email": supplier.get_contact_email()
        }
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


def load_inventory(filename: str = INVENTORY_FILE) -> tuple[list[Product], str]:
    products: list[Product] = []
    suppliers: dict[str, Supplier] = {}
    status: str = "not_found"

    try:
        with open(filename, "r") as file:
            data: Any = json.load(file)

        if not isinstance(data, list):
            return [], "error"

        for item in data:
            products.append(product_from_dict(item, suppliers))
        status = "loaded"

    except FileNotFoundError:
        products = []
        status = "not_found"
    except (json.JSONDecodeError, KeyError, TypeError, ValueError):
        products = []
        status = "error"

    return products, status


def save_inventory(products: Sequence[Product], filename: str = INVENTORY_FILE) -> None:
    data: list[dict[str, Any]] = []
    for product in products:
        data.append(product_to_dict(product))

    with open(filename, "w") as file:
        json.dump(data, file, indent=4)
