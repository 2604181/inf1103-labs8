"""
INF1103 Week 9 - Inventory Manager (OOP: inheritance, abstraction, interfaces)
Responsibility: display the menu, get user input, call Inventory methods.
"""
from inventory import Inventory
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from can_be_shipped import CanBeShipped
from file_handling import load_inventory, save_inventory, INVENTORY_FILE


def get_valid_int(prompt):
    while True:
        user_input = input(prompt)
        if user_input.isdigit():
            return int(user_input)
        print("Error. Please enter a valid whole number (0 or more).")


def get_valid_float(prompt):
    while True:
        user_input = input(prompt)
        try:
            number = float(user_input)
        except ValueError:
            print("Error. Please enter a valid number.")
            continue
        if number < 0:
            print("Error. Value cannot be negative.")
            continue
        return number


def get_product_type_choice():
    while True:
        choice = input("Product Type (1 = Physical, 2 = Digital): ").strip()
        if choice == "1" or choice == "2":
            return choice
        print("Error. Please enter 1 for Physical or 2 for Digital.")


def display_menu():
    print("----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("----------------------------")


def main():
    """
    Main function to run inventory manager.
    """
    # local variables
    inventory = Inventory()
    exit_program = False

    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)

    products, status = load_inventory()
    for product in products:
        inventory.add_product(product)

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
        option = input("Enter option: ").strip()

        if option == "1":
            inventory.display_all()

        elif option == "2":
            print("Add New Product")
            product_type = get_product_type_choice()
            product_id = input("Product ID: ").strip().upper()
            name = input("Product Name: ").strip()
            if product_id == "" or name == "":
                print("Error. Product ID and Name cannot be empty.")
            else:
                price = get_valid_float("Price: ")
                stock = get_valid_int("Stock Quantity: ")
                if product_type == "1":
                    weight = get_valid_float("Weight (kg): ")
                    new_product = PhysicalProduct(
                        product_id, name, price, stock, weight
                    )
                else:
                    download_size = get_valid_float("Download Size (MB): ")
                    new_product = DigitalProduct(
                        product_id, name, price, stock, download_size
                    )
                if inventory.add_product(new_product):
                    print("Product added successfully!")
                else:
                    print(f"Error. Product ID {product_id} already exists.")

        elif option == "3":
            print("Update Stock")
            product_id = input("Enter Product ID: ").strip().upper()
            product = inventory.search_product(product_id)
            if product is None:
                print("Product not found.")
            else:
                print("Product Found:")
                print(f"Name: {product.get_name()}")
                print(f"Current Stock: {product.get_stock()}")
                new_stock = get_valid_int("New Stock Quantity: ")
                product.update_stock(new_stock)
                print("Stock updated successfully!")

        elif option == "4":
            print("Search Product")
            product_id = input("Enter Product ID: ").strip().upper()
            product = inventory.search_product(product_id)
            if product is None:
                print("Product not found.")
            else:
                print("Product Found")
                print("-" * 48)
                product.display_information()                print(f"    Fulfilment: {product.get_fulfilment_info()}")
                if isinstance(product, CanBeShipped):
                    cost = product.calculate_shipping_cost()
                    print(f"    Shipping Cost: ${cost:.2f}")
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
