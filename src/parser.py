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
            image_url = self._get_image_url(soup)  # Добавляем извлечение изображения
            print(
                f"Извлечены данные для {url}: name={name}, price={price}, rating={rating}, description={description}, usage={usage}, country={country}, image={image_url}")
            return Product(
                url=url,
                name=name,
                price=price,
                rating=rating,
                description=description,
                usage=usage,
                country=country,
                image_url=image_url  # Передаём URL изображения
            )
        except Exception as e:
            print(f"Error parsing product page {url}: {e}")
            return None

    def _get_name(self, soup):
        try:
            name_tag = soup.select_one("h1[class*='title'], div[class*='name']")
            return name_tag.get_text(strip=True) if name_tag else "Не указано"
        except Exception as e:
            print(f"Ошибка при извлечении названия: {e}")
            return "Не указано"

    def _get_price(self, soup):
        try:
            price_tag = soup.select_one("span[class*='price'], div[class*='price']")
            price = price_tag.get_text(strip=True).replace("₽", "").replace(" ", "") if price_tag else "0"
            return price
        except Exception as e:
            print(f"Ошибка при извлечении цены: {e}")
            return "0"

    def _get_rating(self, soup):
        try:
            rating_tag = soup.select_one("span[class*='rating'], div[class*='rating']")
            return rating_tag.get_text(strip=True) if rating_tag else "0"
        except Exception as e:
            print(f"Ошибка при извлечении рейтинга: {e}")
            return "0"

    def _get_description(self, soup):
        try:
            description_tag = soup.select_one("div[class*='description'], p[class*='description']")
            return description_tag.get_text(strip=True) if description_tag else ""
        except Exception as e:
            print(f"Ошибка при извлечении описания: {e}")
            return ""

    def _get_usage(self, soup):
        try:
            usage_tag = soup.select_one("div[class*='usage'], p[class*='usage'], div[class*='application']")
            return usage_tag.get_text(strip=True) if usage_tag else ""
        except Exception as e:
            print(f"Ошибка при извлечении способа применения: {e}")
            return ""

    def _get_country(self, soup):
        try:
            country_tag = soup.select_one("div[class*='country'], span[class*='country']")
            return country_tag.get_text(strip=True) if country_tag else ""
        except Exception as e:
            print(f"Ошибка при извлечении страны: {e}")
            return ""

    def _get_image_url(self, soup):
        try:
            image_tag = soup.select_one("img[class*='main-image'], img[class*='product-image']")
            image_url = image_tag['src'] if image_tag else ""
            if image_url and not image_url.startswith("http"):
                image_url = "https://goldapple.ru" + image_url
            return image_url
        except Exception as e:
            print(f"Ошибка при извлечении URL изображения: {e}")
            return ""