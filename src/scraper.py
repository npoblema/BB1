import requests
from bs4 import BeautifulSoup
from src.parser import ProductParser
from src.models import Product
import time

class GoldAppleScraper:
    def __init__(self, base_url):
        self.base_url = base_url
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        self.parser = ProductParser()

    def scrape_products(self):
        products = []
        page = 1
        while True:
            url = f"{self.base_url}?p={page}"
            response = self._fetch_page(url)
            if not response:
                break
            soup = BeautifulSoup(response.text, "lxml")
            # Обновлённый селектор (замените на актуальный класс)
            product_cards = soup.select("div.catalog-product")
            if not product_cards:
                print(f"Нет карточек товаров на странице {url}. Прерывание цикла.")  # Для отладки
                break
            for card in product_cards:
                product = self._parse_product_card(card)
                if product:
                    products.append(product)
            page += 1
            time.sleep(1)  # Избегайте перегрузки сервера
        print(f"Найдено {len(product_cards)} карточек на странице {url}")
        return products

    def _fetch_page(self, url):
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None

    def _parse_product_card(self, card):
        product_url = card.select_one("a.catalog-product__link")["href"]  # Обновите селектор
        if not product_url.startswith("http"):
            product_url = "https://goldapple.ru" + product_url
        response = self._fetch_page(product_url)
        if not response:
            return None
        soup = BeautifulSoup(response.text, "lxml")
        return self.parser.parse_product_page(soup, product_url)