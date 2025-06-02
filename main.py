from src.scraper import GoldAppleScraper
from src.exporter import CsvExporter

def main():
    base_url = "https://goldapple.ru/parfjumerija"
    scraper = GoldAppleScraper(base_url)
    products = scraper.scrape_products(max_pages=5, max_cards=5)  # Ограничиваем до 5 карточек
    exporter = CsvExporter(output_path="data/products.csv")
    exporter.export(products)
    print("Scraping completed. Data saved to data/products.csv")

if __name__ == "__main__":
    main()