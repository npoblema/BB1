import unittest
from src.scraper import GoldAppleScraper

class TestGoldAppleScraper(unittest.TestCase):
    def setUp(self):
        self.scraper = GoldAppleScraper("https://goldapple.ru/parfjumerija")

    def test_scrape_products(self):
        products = self.scraper.scrape_products(max_pages=1)
        self.assertIsInstance(products, list)
        if products:
            self.assertTrue(hasattr(products[0], "url"))
            self.assertTrue(hasattr(products[0], "name"))

    def tearDown(self):
        self.scraper.driver.quit()

if __name__ == "__main__":
    unittest.main()