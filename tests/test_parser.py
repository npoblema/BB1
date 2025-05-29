import unittest
from src.parser import ProductParser
from bs4 import BeautifulSoup

class TestProductParser(unittest.TestCase):
    def setUp(self):
        self.parser = ProductParser()
        self.html = """
        <html>
            <h1 class="product__title">Perfume Name</h1>
            <span class="product-price__sum">1 500 ₽</span>
            <div class="rating" data-rating="4.5"></div>
            <div class="product__description">Description text</div>
            <div class="product__usage">Usage text</div>
            <div class="product__country">Страна: Франция</div>
        </html>
        """
        self.soup = BeautifulSoup(self.html, "lxml")

    def test_parse_product_page(self):
        product = self.parser.parse_product_page(self.soup, "https://goldapple.ru/product")
        self.assertEqual(product.name, "Perfume Name")
        self.assertEqual(product.price, "1 500")
        self.assertEqual(product.rating, "4.5")
        self.assertEqual(product.description, "Description text")
        self.assertEqual(product.usage, "Usage text")
        self.assertEqual(product.country, "Франция")

if __name__ == "__main__":
    unittest.main()