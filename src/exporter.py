import pandas as pd

class CsvExporter:
    def __init__(self, output_path):
        self.output_path = output_path

    def export(self, products):
        data = [
            {
                "Ссылка на продукт": p.url,
                "Наименование": p.name,
                "Цена": p.price,
                "Рейтинг пользователей": p.rating,
                "Описание продукта": p.description,
                "Инструкция по применению": p.usage,
                "Страна-производитель": p.country
            }
            for p in products if p
        ]
        df = pd.DataFrame(data)
        df.to_csv(self.output_path, index=False, encoding="utf-8")