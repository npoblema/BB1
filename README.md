# Gold Apple Perfume Scraper

## Описание проекта
Этот проект представляет собой веб-скрапинг-утилиту, разработанную для сбора данных о товарах из раздела "Парфюмерия" интернет-магазина Gold Apple (https://goldapple.ru/parfjumerija). Цель проекта — извлечь информацию о товарах (наименование, цена, рейтинг, описание, инструкции по применению и страну-производителя) и сохранить её в CSV-файл. Данные могут быть использованы для анализа популярности товаров, закупки и продвижения в рекламе.

Проект реализован на Python 3.11 с использованием объектно-ориентированного подхода, регулярных выражений для парсинга и покрыт тестами с уровнем покрытия ≥75%.

---

## Установка

### Требования
- Python 3.11 или выше
- Установленные зависимости (см. ниже)

### Шаги установки
1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/npoblemapi/BB1.git
   cd BB1
   
---

## Возможные проблемы и их решения

### Ошибка доступа к сайту Gold Apple
Если скрипт не может загрузить данные с сайта (например, ошибка `Error fetching...`):
- Проверьте интернет-соединение.
- Убедитесь, что сайт https://goldapple.ru/parfjumerija доступен. Возможно, сайт временно недоступен или заблокирован в вашем регионе.
- Проверьте, не изменилась ли структура сайта (например, классы CSS). В этом случае обновите селекторы в `src/scraper.py` и `src/parser.py`.

### Ошибка с зависимостями
Если возникает ошибка `ModuleNotFoundError`:
- Убедитесь, что вы активировали виртуальное окружение перед запуском:
  - Windows: `venv\Scripts\activate`
  - Linux/Mac: `source venv/bin/activate`
- Переустановите зависимости:
  ```bash
  pip install -r requirements.txt