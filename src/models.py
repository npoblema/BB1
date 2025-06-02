from dataclasses import dataclass

@dataclass
class Product:
    url: str
    name: str
    price: str
    rating: str
    description: str
    usage: str
    country: str
    brand: str = ""