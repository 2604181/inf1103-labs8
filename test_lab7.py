"""
INF1103 Week 9 - Tests for the Lab 7 testing requirements.
Run with:  python test_lab7.py
(Uses a temporary file for the JSON tests, so your real inventory.json is not touched.)
"""
import contextlib
import io
import json
import os
import tempfile
import unittest

from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from can_be_shipped import CanBeShipped
from inventory import Inventory
from file_handling import load_inventory, save_inventory


def capture_output(function):
    """Run a function and return everything it printed."""
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        function()
    return buffer.getvalue()


class TestProductTypes(unittest.TestCase):
    def setUp(self):
        self.physical = PhysicalProduct("P001", "Laptop", 1200.00, 15, 2.5)
        self.digital = DigitalProduct("D001", "Antivirus", 29.99, 100, 350.0)

    # 1. Physical products store and display their weights
    def test_physical_stores_and_displays_weight(self):
        self.assertEqual(self.physical.get_weight(), 2.5)
        output = capture_output(self.physical.display_information)
        self.assertIn("ID: P001 | Name: Laptop | Price: $1200.00 | Stock: 15", output)
        self.assertIn("Weight: 2.50 kg", output)

    # 2. Digital products store and display their download sizes
    def test_digital_stores_and_displays_download_size(self):
        self.assertEqual(self.digital.get_download_size(), 350.0)
        output = capture_output(self.digital.display_information)
        self.assertIn("ID: D001 | Name: Antivirus | Price: $29.99 | Stock: 100", output)
        self.assertIn("Download Size: 350.00 MB", output)

    # 3. Both subclasses implement get_fulfilment_info()
    def test_both_implement_get_fulfilment_info(self):
        self.assertEqual(self.physical.get_fulfilment_info(), "Requires physical shipping.")
        self.assertEqual(self.digital.get_fulfilment_info(), "Delivered digitally via download link.")

    # Inheritance (IS-A) checks
    def test_inheritance(self):
        self.assertTrue(issubclass(PhysicalProduct, Product))
        self.assertTrue(issubclass(DigitalProduct, Product))
        self.assertIsInstance(self.physical, Product)
        self.assertIsInstance(self.digital, Product)

    # 4. The abstract Product class cannot be instantiated directly
    def test_product_cannot_be_instantiated(self):
        with self.assertRaises(TypeError):
            Product("X001", "Generic", 1.0, 1)

    def test_interface_cannot_be_instantiated(self):
        with self.assertRaises(TypeError):
            CanBeShipped()

    # 5. Physical products can calculate shipping costs (different weights)
    def test_shipping_cost_for_different_weights(self):
        expected = {0.0: 5.00, 0.5: 6.00, 1.0: 7.00, 2.5: 10.00, 10.0: 25.00}
        for weight, cost in expected.items():
            product = PhysicalProduct("T", "Test", 1.0, 1, weight)
            self.assertAlmostEqual(product.calculate_shipping_cost(), cost)
            self.assertGreaterEqual(product.calculate_shipping_cost(), 0)

    def test_heavier_products_cost_more_to_ship(self):
        light = PhysicalProduct("L", "Light", 1.0, 1, 1.0)
        heavy = PhysicalProduct("H", "Heavy", 1.0, 1, 8.0)
        self.assertGreater(heavy.calculate_shipping_cost(), light.calculate_shipping_cost())

    def test_physical_implements_interface(self):
        self.assertIsInstance(self.physical, CanBeShipped)

    # 6. Digital products are not required to implement shipping behaviour
    def test_digital_does_not_implement_shipping(self):
        self.assertNotIsInstance(self.digital, CanBeShipped)
        self.assertFalse(hasattr(self.digital, "calculate_shipping_cost"))

    # Encapsulation: the stock is changed through the public method
    def test_update_stock_through_method(self):
        self.physical.update_stock(50)
        self.assertEqual(self.physical.get_stock(), 50)
        self.physical.update_stock(-5)
        self.assertEqual(self.physical.get_stock(), 50)

    def test_negative_weight_or_size_rejected(self):
        with self.assertRaises(ValueError):
            PhysicalProduct("T", "Test", 1.0, 1, -1.0)
        with self.assertRaises(ValueError):
            DigitalProduct("T", "Test", 1.0, 1, -1.0)


class TestInventoryOperations(unittest.TestCase):
    # 7. Inventory operations continue to work
    def setUp(self):
        self.inventory = Inventory()
        self.inventory.add_product(PhysicalProduct("P001", "Laptop", 1200.00, 15, 2.5))
        self.inventory.add_product(DigitalProduct("D001", "Antivirus", 29.99, 100, 350.0))

    def test_add_and_duplicate_rejected(self):
        self.assertTrue(self.inventory.add_product(DigitalProduct("D002", "E-Book", 9.99, 5, 12.5)))
        self.assertFalse(self.inventory.add_product(DigitalProduct("D002", "Other", 1.0, 1, 1.0)))
        self.assertEqual(len(self.inventory.get_products()), 3)

    def test_search(self):
        self.assertEqual(self.inventory.search_product("P001").get_name(), "Laptop")
        self.assertEqual(self.inventory.search_product("D001").get_name(), "Antivirus")
        self.assertIsNone(self.inventory.search_product("P999"))

    def test_update_stock_via_search(self):
        self.inventory.search_product("P001").update_stock(40)
        self.assertEqual(self.inventory.search_product("P001").get_stock(), 40)

    def test_display_all_shows_both_types(self):
        output = capture_output(self.inventory.display_all)
        self.assertIn("Name: Laptop", output)
        self.assertIn("Weight: 2.50 kg", output)
        self.assertIn("Name: Antivirus", output)
        self.assertIn("Download Size: 350.00 MB", output)


class TestJsonPersistence(unittest.TestCase):
    # 8. JSON saving and loading preserve the correct product types
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.folder.name, "inventory.json")

    def tearDown(self):
        self.folder.cleanup()

    def test_round_trip_preserves_types_and_attributes(self):
        original = [
            PhysicalProduct("P001", "Laptop", 1200.00, 15, 2.5),
            DigitalProduct("D001", "Antivirus", 29.99, 100, 350.0),
        ]
        save_inventory(original, self.path)

        with open(self.path) as file:
            saved = json.load(file)
        self.assertEqual(saved[0]["type"], "physical")
        self.assertEqual(saved[1]["type"], "digital")

        loaded, status = load_inventory(self.path)
        self.assertEqual(status, "loaded")
        self.assertIsInstance(loaded[0], PhysicalProduct)
        self.assertIsInstance(loaded[1], DigitalProduct)
        self.assertEqual(loaded[0].get_weight(), 2.5)
        self.assertEqual(loaded[1].get_download_size(), 350.0)
        self.assertEqual(loaded[0].get_stock(), 15)
        self.assertEqual(loaded[1].get_price(), 29.99)

    def test_missing_file_starts_empty(self):
        products, status = load_inventory(self.path)
        self.assertEqual((products, status), ([], "not_found"))

    def test_corrupt_file_starts_empty(self):
        with open(self.path, "w") as file:
            file.write("{bad")
        self.assertEqual(load_inventory(self.path), ([], "error"))

    def test_unknown_or_missing_type_is_rejected(self):
        for bad in ([{"id": "X", "name": "N", "price": 1, "stock": 1, "type": "subscription"}],
                    [{"id": "X", "name": "N", "price": 1, "stock": 1}]):
            with open(self.path, "w") as file:
                json.dump(bad, file)
            self.assertEqual(load_inventory(self.path), ([], "error"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
