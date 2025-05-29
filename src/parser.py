import re
from src.models import Product

class ProductParser:
    def parse_product_page(self, soup, url):
        try:
            name = self._get_name(soup)
            price = self._get_price(soup)
            rating = self._get_rating(soup)
            description = self._get_description(soup)
            usage = self._get_usage(soup)
            country = self._get_country(soup)
            return Product(
                url=url,
                name=name,
                price=price,
                rating=rating,
                description=description,
                usage=usage,
                country=country
            )
        except Exception as e:
            print(f"Error parsing product page {url}: {e}")
            return None

    def _get_name(self, soup):
        name_tag = soup.select_one("h1.product__title")
        return name_tag.text.strip() if name_tag else "N/A"

    def _get_price(self, soup):
        price_tag = soup.select_one("span.product-price__sum")
        if price_tag:
            price_text = price_tag.text.strip()
            match = re.search(r"[\d\s]+", price_text)
            return match.group().strip() if match else "N/A"
        return "N/A"

    def _get_rating(self, soup):
        rating_tag = soup.select_one("div.rating")
        if rating_tag:
            rating_text = rating_tag.get("data-rating", "N/A")
            match = re.search(r"\d+\.\d+", rating_text)
            return match.group() if match else "N/A"
        return "N/A"

    def _get_description(self, soup):
        desc_tag = soup.select_one("div.product__description")
        return desc_tag.text.strip() if desc_tag else "N/A"

    def _get_usage(self, soup):
        usage_tag = soup.select_one("div.product__usage")
        return usage_tag.text.strip() if usage_tag else "N/A"

    def _get_country(self, soup):
        country_tag = soup.select_one("div.product__country")
        if country_tag:
            country_text = country_tag.text.strip()
            match = re.search(r"Страна:\s*([\w\s]+)", country_text, re.IGNORECASE)
            return match.group(1).strip() if match else "N/A"
        return "N/A"