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

            print(f"Извлечены данные со страницы товара: url={url}, description={description}, usage={usage}, country={country}")
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
        name_tag = soup.select_one("h1[class*='title'], div[class*='name']")
        if not name_tag:
            # Попробуем извлечь название как комбинацию бренда и модели
            brand_tag = soup.select_one("span.zHshR")
            model_tag = soup.select_one("span.pwPQH")
            brand = brand_tag.get_text(strip=True) if brand_tag else ""
            model = model_tag.get_text(strip=True) if model_tag else ""
            return f"{brand} {model}" if brand or model else "Не указано"
        return name_tag.get_text(strip=True)

    def _get_price(self, soup):
        price_tag = soup.select_one("div.QNXB7")
        price = price_tag.get_text(strip=True).replace("₽", "").replace(" ", "") if price_tag else "0"
        return price

    def _get_rating(self, soup):
        rating_tag = soup.select_one("div.NHN0t")
        return rating_tag.get_text(strip=True) if rating_tag else "0"

    def _get_description(self, soup):
        description_tag = soup.select_one("div[class*='description'], p[class*='description'], div[class*='product-description']")
        if description_tag:
            text = description_tag.get_text(strip=True)
            return re.sub(r'\s+', ' ', text)  # Очищаем лишние пробелы
        return ""

    def _get_usage(self, soup):
        usage_tag = soup.select_one("div[class*='usage'], p[class*='usage'], div[class*='application'], div[class*='how-to-use']")
        if usage_tag:
            text = usage_tag.get_text(strip=True)
            return re.sub(r'\s+', ' ', text)
        return ""

    def _get_country(self, soup):
        country_tag = soup.select_one("div[class*='country'], span[class*='country'], div[class*='specifications'] span")
        if country_tag:
            text = country_tag.get_text(strip=True)
            # Проверяем, содержит ли текст информацию о стране
            if any(country.lower() in text.lower() for country in ["россия", "франция", "италия", "сша"]):
                return re.sub(r'\s+', ' ', text)
        return ""