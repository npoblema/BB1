import unittest
from bs4 import BeautifulSoup
from src.parser import ProductParser

class TestProductParser(unittest.TestCase):
    def setUp(self):
        self.parser = ProductParser()

    def test_parse_product_page(self):
        html = """
        <div class="title">Product Name</div>
        <span class="price">1000 ₽</span>
        <div class="description">This is a description.</div>
        """
        soup = BeautifulSoup(html, "html.parser")
        product = self.parser.parse_product_page(soup, "http://example.com")
        self.assertEqual(product.name, "Product Name")
        self.assertEqual(product.price, "1000")
        self.assertEqual(product.description, "This is a description.")

if __name__ == "__main__":
    unittest.main()