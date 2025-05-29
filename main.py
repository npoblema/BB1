from src.scraper import GoldAppleScraper
from src.exporter import CsvExporter

def main():
    base_url = "https://goldapple.ru/parfjumerija"
    scraper = GoldAppleScraper(base_url)
    products = scraper.scrape_products()
    exporter = CsvExporter("data/products.csv")
    exporter.export(products)
    print("Scraping completed. Data saved to data/products.csv")

if __name__ == "__main__":
    main()