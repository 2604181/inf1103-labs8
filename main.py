"""
INF1103 Week 10 - Inventory Manager (OOP: relationships, type hints, LSP)
Responsibility: display the menu, get user input, call Inventory methods.
"""
from inventory import Inventory
from product import Product
from supplier import Supplier
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from can_be_shipped import CanBeShipped
from file_handling import load_inventory, save_inventory, INVENTORY_FILE


def get_valid_int(prompt: str) -> int:
    while True:
        user_input: str = input(prompt)
        if user_input.isdigit():
            return int(user_input)
        print("Error. Please enter a valid whole number (0 or more).")


def get_valid_float(prompt: str) -> float:
    while True:
        user_input: str = input(prompt)
        try:
            number: float = float(user_input)
        except ValueError:
            print("Error. Please enter a valid number.")
            continue
        if number < 0:
            print("Error. Value cannot be negative.")
            continue
        return number


def get_non_empty_text(prompt: str) -> str:
    while True:
        text: str = input(prompt).strip()
        if text != "":
            return text
        print("Error. This field cannot be empty.")


def get_valid_email(prompt: str) -> str:
    while True:
        email: str = input(prompt).strip()
        if "@" in email and "." in email:
            return email
        print("Error. Please enter a valid email address.")


def get_product_type_choice() -> str:
    while True:
        choice: str = input("Product Type (1 = Physical, 2 = Digital): ").strip()
        if choice == "1" or choice == "2":
            return choice
        print("Error. Please enter 1 for Physical or 2 for Digital.")


def build_supplier_lookup(products: list[Product]) -> dict[str, Supplier]:
    """Collect the suppliers the loaded products already refer to (one per id)."""
    suppliers: dict[str, Supplier] = {}
    for product in products:
        supplier: Supplier = product.get_supplier()
        suppliers[supplier.get_supplier_id()] = supplier
    return suppliers


def get_supplier(suppliers: dict[str, Supplier]) -> Supplier:
    """Reuse a known supplier, or create a new independent Supplier object."""
    supplier_id: str = get_non_empty_text("Supplier ID: ").upper()
    if supplier_id in suppliers:
        existing: Supplier = suppliers[supplier_id]
        print(f"Using existing supplier: {existing.get_name()}")
        return existing

    name: str = get_non_empty_text("Supplier Name: ")
    email: str = get_valid_email("Supplier Email: ")
    return Supplier(supplier_id, name, email)


def display_menu() -> None:
    print("----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("----------------------------")


def main() -> None:
    """
    Main function to run inventory manager.
    """
    # local variables
    inventory: Inventory = Inventory()
    exit_program: bool = False

    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)

    products: list[Product]
    status: str
    products, status = load_inventory()
    for product in products:
        inventory.add_product(product)
    suppliers: dict[str, Supplier] = build_supplier_lookup(products)

    if status == "loaded":
        print(f"{INVENTORY_FILE} found.")
        print("Inventory loaded successfully.")
    elif status == "not_found":
        print(f"{INVENTORY_FILE} not found.")
        print("Starting with an empty inventory.")
    else:
        print(f"{INVENTORY_FILE} could not be read.")
        print("Starting with an empty inventory.")

    display_menu()

    while not exit_program:
        option: str = input("Enter option: ").strip()

        if option == "1":
            inventory.display_all()

        elif option == "2":
            print("Add New Product")
            product_type: str = get_product_type_choice()
            product_id: str = input("Product ID: ").strip().upper()
            name: str = input("Product Name: ").strip()
            if product_id == "" or name == "":
                print("Error. Product ID and Name cannot be empty.")
            else:
                price: float = get_valid_float("Price: ")
                stock: int = get_valid_int("Stock Quantity: ")
                supplier: Supplier = get_supplier(suppliers)
                new_product: Product
                if product_type == "1":
                    weight: float = get_valid_float("Weight (kg): ")
                    new_product = PhysicalProduct(
                        product_id, name, price, stock, supplier, weight
                    )
                else:
                    download_size: float = get_valid_float("Download Size (MB): ")
                    new_product = DigitalProduct(
                        product_id, name, price, stock, supplier, download_size
                    )
                if inventory.add_product(new_product):
                    suppliers[supplier.get_supplier_id()] = supplier
                    print("Product added successfully!")
                else:
                    print(f"Error. Product ID {product_id} already exists.")

        elif option == "3":
            print("Update Stock")
            product_id = input("Enter Product ID: ").strip().upper()
            found: Product | None = inventory.search_product(product_id)
            if found is None:
                print("Product not found.")
            else:
                print("Product Found:")
                print(f"Name: {found.get_name()}")
                print(f"Current Stock: {found.get_stock()}")
                new_stock: int = get_valid_int("New Stock Quantity: ")
                found.update_stock(new_stock)
                print("Stock updated successfully!")

        elif option == "4":
            print("Search Product")
            product_id = input("Enter Product ID: ").strip().upper()
            found = inventory.search_product(product_id)
            if found is None:
                print("Product not found.")
            else:
                print("Product Found")
                print("-" * 48)
                found.display_information()
                print(f"    Fulfilment: {found.get_fulfilment_info()}")
                if isinstance(found, CanBeShipped):
                    cost: float = found.calculate_shipping_cost()
                    print(f"    Shipping Cost: ${cost:.2f}")
                print("    Supplier:")
                found.get_supplier().display_information()
                print("-" * 48)

        elif option == "5":
            print("Saving inventory...")
            save_inventory(inventory.get_products())
            print(f"Inventory saved successfully to {INVENTORY_FILE}.")

        elif option == "6":
            print("Saving inventory before exit...")
            save_inventory(inventory.get_products())
            print("Inventory saved successfully.")
            print("Thank you for using Inventory Management System.")
            print("Program terminated.")
            exit_program = True

        else:
            print("Invalid option. Please enter a number from 1 to 6.")


# __name__ (Program Entry Point)
if __name__ == "__main__":
    main()
