"""
INF1103 Week 10 - Demonstrations for the Lab 8 'Predict first' activities.

BEFORE running a section, write down your prediction. Then run it:

    python demo_lab8.py association      (Section 2.2)
    python demo_lab8.py aggregation      (Section 3.2)
    python demo_lab8.py composition      (Section 4.3)
    python demo_lab8.py lsp              (Section 6.2)
    python demo_lab8.py polymorphism     (Section 7.2)
    python demo_lab8.py                  (runs all sections)
"""
import sys

from supplier import Supplier
from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from inventory import Inventory
from order import Order


def make_products(supplier: Supplier) -> tuple[PhysicalProduct, DigitalProduct]:
    laptop: PhysicalProduct = PhysicalProduct("P001", "Laptop", 1200.00, 15, supplier, 2.5)
    antivirus: DigitalProduct = DigitalProduct("D001", "Antivirus", 29.99, 100, supplier, 350.0)
    return laptop, antivirus


def heading(title: str) -> None:
    print()
    print("=" * 60)
    print(title)
    print("=" * 60)


def demo_association() -> None:
    heading("SECTION 2.2 - ASSOCIATION: Supplier and Product")
    supplier: Supplier = Supplier("S001", "TechSource Pte Ltd", "sales@techsource.sg")
    laptop, antivirus = make_products(supplier)

    print("Supplier through the physical product:")
    laptop.get_supplier().display_information()
    print("Supplier through the digital product:")
    antivirus.get_supplier().display_information()
    print("Same Supplier object for both products?",
          laptop.get_supplier() is antivirus.get_supplier())

    print("\nNow running: del supplier")
    del supplier
    print("Can each product still show its supplier?")
    laptop.get_supplier().display_information()
    antivirus.get_supplier().display_information()


def demo_aggregation() -> None:
    heading("SECTION 3.2 - AGGREGATION: Inventory and Product")
    supplier: Supplier = Supplier("S001", "TechSource Pte Ltd", "sales@techsource.sg")
    laptop, _ = make_products(supplier)       # Product created BEFORE any Inventory
    inventory_a: Inventory = Inventory()
    inventory_b: Inventory = Inventory()

    inventory_a.add_product(laptop)
    print("Added to Inventory A. A holds:", [p.get_name() for p in inventory_a.products])

    inventory_a.remove_product("P001")
    print("Removed from Inventory A. A holds:", [p.get_name() for p in inventory_a.products])
    print("Can the Product still be used?")
    laptop.display_information()
    laptop.update_stock(20)
    print("After update_stock(20), stock =", laptop.get_stock())

    inventory_b.add_product(laptop)
    print("Added the SAME object to Inventory B. B holds:",
          [p.get_name() for p in inventory_b.products])
    print("Is it the same object?", inventory_b.find_product("P001") is laptop)

    inventory_b.remove_product("P001")
    print("Inventory B emptied. Product still exists:", laptop.get_name(), "- stock", laptop.get_stock())


def demo_composition() -> None:
    heading("SECTION 4.3 - COMPOSITION: Order and OrderLine")
    supplier: Supplier = Supplier("S001", "TechSource Pte Ltd", "sales@techsource.sg")
    laptop, antivirus = make_products(supplier)

    order_1: Order = Order("O001")
    order_1.add_order_line(laptop, 1)
    order_1.add_order_line(antivirus, 2)

    print(f"Order {order_1.get_order_id()} lines:")
    for product, quantity, subtotal in order_1.get_order_lines():
        print(f"  {product.get_name()} x {quantity} = ${subtotal:.2f}")
    print(f"Order total: ${order_1.calculate_total():.2f}")

    order_2: Order = Order("O002")
    order_2.add_order_line(laptop, 3)
    print(f"\nSame Product added to a second order {order_2.get_order_id()}.")

    # Peeking at the private lists with name mangling, ONLY to answer the
    # 'Predict first' question. Normal code must never do this.
    line_1 = order_1._Order__order_lines[0]    # type: ignore[attr-defined]
    line_2 = order_2._Order__order_lines[0]    # type: ignore[attr-defined]
    print("Same Product object in both orders?",
          line_1.get_product() is line_2.get_product())
    print("Same OrderLine object in both orders?", line_1 is line_2)
    print("Distinct OrderLine objects:", id(line_1) != id(line_2),
          "| distinct Product objects:", 1 if line_1.get_product() is line_2.get_product() else 2)

    print("\nRemoving line 0 from order 1 (an Order method) ...")
    order_1.remove_order_line(0)
    print(f"Order {order_1.get_order_id()} total now: ${order_1.calculate_total():.2f}")
    print("The Product itself is untouched:", laptop.get_name(), "still exists")


def show_product_details(product: Product) -> None:
    product.display_information()
    print(product.get_fulfilment_info())


def restock(product: Product, quantity: int) -> None:
    """Code written against the Product abstraction only."""
    product.update_stock(quantity)
    print(f"  {product.get_name()} stock is now {product.get_stock()}")


class BadDigitalProduct(DigitalProduct):
    """The teammate's design from the 'Diagnose' question. It breaks LSP."""
    def update_stock(self, quantity: int) -> None:
        raise NotImplementedError("Digital products have no stock")


def demo_lsp() -> None:
    heading("SECTION 6.2 - LSP: show_product_details(product: Product)")
    supplier: Supplier = Supplier("S001", "TechSource Pte Ltd", "sales@techsource.sg")
    laptop, antivirus = make_products(supplier)

    print("--- PhysicalProduct passed as a Product ---")
    show_product_details(laptop)
    print("--- DigitalProduct passed as a Product ---")
    show_product_details(antivirus)

    print("\nSame update_stock() contract for both subclasses:")
    restock(laptop, 50)
    restock(antivirus, 75)
    restock(laptop, -5)
    restock(antivirus, -5)

    print("\n--- The Diagnose example: a subclass that breaks the parent's contract ---")
    bad: BadDigitalProduct = BadDigitalProduct("D002", "Bad Product", 9.99, 10, supplier, 1.0)
    try:
        restock(bad, 20)
    except NotImplementedError as error:
        print(f"  LSP violated! Code that works for any Product crashed: {error}")


def demo_polymorphism() -> None:
    heading("SECTION 7.2 - POLYMORPHISM: one collection, different behaviour")
    supplier: Supplier = Supplier("S001", "TechSource Pte Ltd", "sales@techsource.sg")
    laptop, antivirus = make_products(supplier)
    mouse: PhysicalProduct = PhysicalProduct("P002", "Mouse", 25.50, 40, supplier, 0.1)

    inventory: Inventory = Inventory()
    inventory.add_product(laptop)
    inventory.add_product(antivirus)
    inventory.add_product(mouse)

    for product in inventory.products:      # no isinstance(), no separate loops
        product.display_information()
        print(product.get_fulfilment_info())


SECTIONS = {
    "association": demo_association,
    "aggregation": demo_aggregation,
    "composition": demo_composition,
    "lsp": demo_lsp,
    "polymorphism": demo_polymorphism,
}

if __name__ == "__main__":
    if len(sys.argv) > 1:
        name = sys.argv[1].lower()
        if name in SECTIONS:
            SECTIONS[name]()
        else:
            print("Unknown section. Choose from:", ", ".join(SECTIONS))
    else:
        for section in SECTIONS.values():
            section()
