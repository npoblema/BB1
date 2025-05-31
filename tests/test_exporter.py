import unittest
import os
import pandas as pd
from src.exporter import CsvExporter
from src.models import Product

class TestCsvExporter(unittest.TestCase):
    def setUp(self):
        self.exporter = CsvExporter("test_products.csv")
        self.products = [
            Product(
                url="https://goldapple.ru",
                name="Perfume Name",
                price="1500",
                rating="4.5",
                description="Description",
                usage="Usage",
                country="France"
            )
        ]

    def test_export(self):
        self.exporter.export(self.products)
        self.assertTrue(os.path.exists("test_products.csv"))
        df = pd.read_csv("test_products.csv")
        self.assertEqual(df.iloc[0]["Наименование"], "Perfume Name")
        os.remove("test_products.csv")

if __name__ == "__main__":
    unittest.main()