import requests
from bs4 import BeautifulSoup
from src.parser import ProductParser
from src.models import Product
import time

class GoldAppleScraper:
    def __init__(self, base_url):
        self.base_url = base_url
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
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
            product_cards = soup.select("div.product-card")
            if not product_cards:
                break
            for card in product_cards:
                product = self._parse_product_card(card)
                if product:
                    products.append(product)
            page += 1
            time.sleep(1)  # Avoid overwhelming the server
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
        product_url = card.select_one("a.product-card__link")["href"]
        if not product_url.startswith("http"):
            product_url = "https://goldapple.ru" + product_url
        response = self._fetch_page(product_url)
        if not response:
            return None
        soup = BeautifulSoup(response.text, "lxml")
        return self.parser.parse_product_page(soup, product_url)