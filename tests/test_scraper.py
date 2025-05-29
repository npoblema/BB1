import unittest
from unittest.mock import patch, Mock
import requests
from src.scraper import GoldAppleScraper

class TestGoldAppleScraper(unittest.TestCase):
    def setUp(self):
        self.scraper = GoldAppleScraper("https://goldapple.ru/parfjumerija")

    @patch("requests.get")
    def test_fetch_page_success(self, mock_get):
        mock_response = Mock()
        mock_response.text = "<html></html>"
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        response = self.scraper._fetch_page("https://goldapple.ru/parfjumerija")
        self.assertIsNotNone(response)
        self.assertEqual(response.text, "<html></html>")

    @patch("requests.get")
    def test_fetch_page_failure(self, mock_get):
        # Имитируем исключение, которое ожидает метод
        mock_get.side_effect = requests.RequestException("Request failed")
        response = self.scraper._fetch_page("https://goldapple.ru/parfjumerija")
        self.assertIsNone(response)  # Проверяем, что метод возвращает None при ошибке

    @patch("src.scraper.GoldAppleScraper._fetch_page")
    @patch("src.scraper.GoldAppleScraper._parse_product_card")
    def test_scrape_products(self, mock_parse_product_card, mock_fetch_page):
        # Имитируем успешный запрос с пустым списком продуктов
        mock_fetch_page.side_effect = [
            Mock(text="<html><div class='product-card'></div></html>"),
            None
        ]
        mock_parse_product_card.return_value = None  # Симулируем отсутствие данных о продукте
        products = self.scraper.scrape_products()
        self.assertEqual(len(products), 0)  # Ожидаем пустой список

if __name__ == "__main__":
    unittest.main()