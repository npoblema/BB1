import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.parser import ProductParser
from src.models import Product

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
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument(f"user-agent={self.headers['User-Agent']}")
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument("--enable-unsafe-swiftshader")
        chrome_options.add_argument("--disable-software-rasterizer")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--window-size=1920,1080")
        self.driver = webdriver.Chrome(options=chrome_options)

    def scrape_products(self, max_pages=5, max_cards=5):
        products = []
        page = 1
        max_attempts = 3
        while page <= max_pages:
            for attempt in range(max_attempts):
                try:
                    url = f"{self.base_url}?p={page}"
                    response = self._fetch_page(url)
                    if not response:
                        print(f"Попытка {attempt + 1}/{max_attempts} не удалась: {url}. Переход к следующей странице.")
                        break

                    # Используем Selenium для поиска карточек
                    wait = WebDriverWait(self.driver, 10)
                    product_cards = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "article")))
                    if not product_cards:
                        print(f"Нет карточек товаров на странице {url}. Прерывание цикла.")
                        break
                    print(f"Найдено {len(product_cards)} карточек на странице {url}")

                    # Сохраняем HTML всех карточек перед обработкой
                    card_htmls = []
                    for card in product_cards:
                        try:
                            card_html = card.get_attribute("outerHTML")
                            if card_html:
                                card_htmls.append(card_html)
                        except StaleElementReferenceException:
                            print("Stale element при извлечении HTML карточки. Пропускаем.")
                            continue

                    # Обрабатываем сохранённые HTML карточек с ограничением
                    for card_html in card_htmls:
                        product = self._parse_product_card(card_html)
                        if product:
                            # Переходим на страницу товара для извлечения дополнительных данных
                            product_page_response = self._fetch_page(product.url)
                            if product_page_response:
                                soup = BeautifulSoup(product_page_response, "lxml")
                                detailed_product = self.parser.parse_product_page(soup, product.url)
                                if detailed_product:
                                    product.description = detailed_product.description
                                    product.usage = detailed_product.usage
                                    product.country = detailed_product.country
                            products.append(product)

                        # Проверяем, достигли ли лимита карточек
                        if len(products) >= max_cards:
                            self.driver.quit()
                            print(f"Собрано {len(products)} товаров (достигнут лимит)")
                            return products

                    page += 1
                    time.sleep(3)
                    break
                except (WebDriverException, TimeoutException) as e:
                    print(f"Ошибка Selenium на попытке {attempt + 1}/{max_attempts}: {e}")
                    if attempt == max_attempts - 1:
                        print(f"Все попытки загрузки {url} не удались.")
                        break
                    time.sleep(3)
        self.driver.quit()
        print(f"Собрано {len(products)} товаров")
        return products

    def _fetch_page(self, url):
        try:
            self.driver.get(url)
            scroll_pause_time = 3
            last_height = self.driver.execute_script("return document.body.scrollHeight")
            while True:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(scroll_pause_time)
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height
            time.sleep(3)
            page_source = self.driver.page_source
            if "captcha" in page_source.lower() or "access denied" in page_source.lower():
                print(f"Обнаружена CAPTCHA или ограничение доступа на {url}")
                return None
            print(f"Статус загрузки для {url}: страница отрендерена")
            return page_source
        except WebDriverException as e:
            print(f"Error fetching {url}: {e}")
            return None

    def _parse_product_card(self, card_html):
        try:
            soup = BeautifulSoup(card_html, "html.parser")

            # Извлекаем ссылку
            link_tag = soup.find("a")
            if not link_tag or "href" not in link_tag.attrs:
                return None
            product_url = "https://goldapple.ru" + link_tag["href"]

            # Извлекаем название
            name_tag = soup.select_one("span.pwPQH")
            name = name_tag.get_text(strip=True) if name_tag else "Не указано"

            # Извлекаем бренд
            brand_tag = soup.select_one("span.zHshR")
            brand = brand_tag.get_text(strip=True) if brand_tag else ""

            # Извлекаем цену
            # Ищем цену в блоке с классом XKY7d (основная цена, а не рассрочка)
            price_block = soup.select_one("div.XKY7d div.QNXB7")
            if price_block:
                price = price_block.get_text(strip=True).replace("₽", "").replace(" ", "")
            else:
                # Альтернативный способ через meta[itemprop="price"]
                price_meta = soup.select_one("meta[itemprop='price']")
                price = price_meta["content"] if price_meta else "0"

            # Извлекаем рейтинг
            rating_tag = soup.select_one("div.NHN0t")
            rating = rating_tag.get_text(strip=True) if rating_tag else "0"
            try:
                if float(rating) > 5:
                    rating = "0"
            except ValueError:
                rating = "0"

            print(f"Извлечены данные из карточки: name={name}, brand={brand}, price={price}, rating={rating}, url={product_url}")
            return Product(product_url, name, price, rating, description="", usage="", country="", brand=brand)
        except Exception as e:
            print(f"Ошибка при парсинге карточки товара: {e}")
            return None