from bs4 import BeautifulSoup
from src.parser import ProductParser
from src.models import Product
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException

class GoldAppleScraper:
    def __init__(self, base_url):
        self.base_url = base_url
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "Referer": "https://goldapple.ru/"
        }
        self.parser = ProductParser()
        # Настройка Selenium
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Запуск в фоновом режиме
        chrome_options.add_argument("--disable-gpu")  # Отключаем GPU для устранения ошибок
        chrome_options.add_argument("--no-sandbox")  # Для Windows
        chrome_options.add_argument("--disable-dev-shm-usage")  # Для обхода ограничений памяти
        chrome_options.add_argument(f"user-agent={self.headers['User-Agent']}")
        chrome_options.add_argument("--ignore-certificate-errors")  # Игнорировать ошибки SSL
        chrome_options.add_argument("--enable-unsafe-webgl")  # Разрешаем небезопасный WebGL
        chrome_options.add_argument("--window-size=1920,1080")  # Устанавливаем размер окна
        self.driver = webdriver.Chrome(options=chrome_options)

    def scrape_products(self):
        products = []
        page = 1
        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                url = f"{self.base_url}?p={page}"
                response = self._fetch_page(url)
                if not response:
                    print(f"Попытка {attempt + 1}/{max_attempts} не удалась: {url}. Переход к следующей странице.")
                    continue
                soup = BeautifulSoup(response, "lxml")
                # Ищем все ссылки на товары и их родительские элементы
                product_links = soup.select("a[href*='/product']")
                product_cards = [link.parent for link in product_links if link.parent]
                if not product_cards:
                    print(f"Нет карточек товаров на странице {url}. Прерывание цикла.")
                    break
                print(f"Найдено {len(product_cards)} карточек на странице {url}")
                for card in product_cards:
                    product = self._parse_product_card(card)
                    if product:
                        products.append(product)
                page += 1
                time.sleep(2)  # Увеличенная задержка
            except WebDriverException as e:
                print(f"Ошибка Selenium на попытке {attempt + 1}/{max_attempts}: {e}")
                if attempt == max_attempts - 1:
                    print(f"Все попытки загрузки {url} не удались.")
                    break
                time.sleep(2)  # Ждём перед следующей попыткой
        self.driver.quit()  # Закрываем браузер после завершения
        print(f"Собрано {len(products)} товаров")
        return products

    def _fetch_page(self, url):
        try:
            self.driver.get(url)
            # Прокручиваем страницу несколько раз для полной загрузки контента
            scroll_pause_time = 2
            last_height = self.driver.execute_script("return document.body.scrollHeight")
            while True:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(scroll_pause_time)
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height
            time.sleep(2)  # Дополнительная задержка после последней прокрутки
            page_source = self.driver.page_source
            # Проверяем, есть ли CAPTCHA или ошибка
            if "captcha" in page_source.lower() or "access denied" in page_source.lower():
                print(f"Обнаружена CAPTCHA или ограничение доступа на {url}")
                return None
            print(f"Статус загрузки для {url}: страница отрендерена")
            print(f"Первые 2000 символов ответа: {page_source[:2000]}")  # Расширенный вывод
            return page_source
        except WebDriverException as e:
            print(f"Error fetching {url}: {e}")
            return None

    def _parse_product_card(self, card):
        try:
            # Извлекаем название товара
            name_tag = card.select_one("a[class*='title'], span[class*='name'], div[class*='name']")
            name = name_tag.get_text(strip=True) if name_tag else "Не указано"

            # Извлекаем бренд (если есть)
            brand_tag = card.select_one("span[class*='brand'], div[class*='brand']")
            brand = brand_tag.get_text(strip=True) if brand_tag else ""

            # Извлекаем цену
            price_tag = card.select_one("span[class*='price'], div[class*='price']")
            price = price_tag.get_text(strip=True).replace("₽", "").replace(" ", "") if price_tag else "0"

            # Извлекаем рейтинг (если есть)
            rating_tag = card.select_one("span[class*='rating'], div[class*='rating']")
            rating = rating_tag.get_text(strip=True) if rating_tag else "0"

            # Извлекаем ссылку на товар
            link_tag = card.select_one("a[href*='/product']")
            product_url = link_tag['href'] if link_tag else ""
            if product_url and not product_url.startswith("http"):
                product_url = "https://goldapple.ru" + product_url

            # Извлекаем URL изображения (если есть)
            image_tag = card.select_one("img[src]")
            image_url = image_tag['src'] if image_tag else ""
            if image_url and not image_url.startswith("http"):
                image_url = "https://goldapple.ru" + image_url

            print(f"Извлечены данные из карточки: name={name}, brand={brand}, price={price}, rating={rating}, url={product_url}, image={image_url}")
            return Product(product_url, name, price, rating, description="", usage="", country="", brand=brand, image_url=image_url)
        except Exception as e:
            print(f"Ошибка при парсинге карточки товара: {e}")
            return None

    def parse_product_page(self, soup, url):
        # Делегируем парсинг страницы товара ProductParser
        return self.parser.parse_product_page(soup, url)