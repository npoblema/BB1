import unittest
import os
from src.exporter import CsvExporter
from src.models import Product

class TestCsvExporter(unittest.TestCase):
    def setUp(self):
        self.exporter = CsvExporter("test_products.csv")
        self.products = [
            Product(
                url="http://example.com",
                name="Test Product",
                price="1000",
                rating="4.5",
                description="Description",
                usage="Usage",
                country="Country"
            )
        ]

    def test_export(self):
        self.exporter.export(self.products)
        self.assertTrue(os.path.exists("test_products.csv"))
        os.remove("test_products.csv")

if __name__ == "__main__":
    unittest.main()