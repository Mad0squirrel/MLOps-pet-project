import re
from abc import ABC, abstractmethod

import bs4


class AbstractHandler(ABC):
    @abstractmethod
    def get_info(self, soup: bs4.BeautifulSoup) -> str or None:
        pass


class AboutApartmentBlockHandler(AbstractHandler):
    def __init__(self, key_word):
        self.key_word = key_word

    def get_info(self, soup: bs4.BeautifulSoup) -> str or None:
        items = soup.select('ul.params-paramsList-_awNW > li')
        for item in items:
            key = item.find('span', class_='styles-module-noAccent-l9CMS')
            if key and self.key_word in key.text:
                full_text = item.get_text(separator=" ", strip=True)
                cleaned_value = full_text.replace(self.key_word, "").strip(" : ")
                return cleaned_value
        return None


class AboutHouseBlockHandler(AbstractHandler):
    def __init__(self, key_word):
        self.key_word = key_word

    def get_info(self, soup: bs4.BeautifulSoup) -> str or None:
        items = soup.select('ul.params-paramsList-_awNW > li')
        for item in items:
            key = item.find('span', class_='styles-module-noAccent-l9CMS')
            if key and self.key_word in key.text:
                full_text = item.get_text(separator=" ", strip=True)
                cleaned_value = full_text.replace(self.key_word, "").strip(" : ")
                return cleaned_value
        return None


class EmptyHandler(AbstractHandler):
    def get_info(self, soup: bs4.BeautifulSoup) -> str or None:
        return None


class PhysAddressHandler(AbstractHandler):
    def get_info(self, soup: bs4.BeautifulSoup) -> str or None:
        geo_block = soup.select_one("span.style-item-address__string-wt61A")
        address = geo_block.text.strip().replace("\n", "|")
        return address


class NFloorsHandler(AbstractHandler):
    def get_info(self, soup: bs4.BeautifulSoup) -> str or None:
        text = soup.text
        index_begin_number = re.search("/", text).span()[1]
        index_end_number = re.search(" ", text[index_begin_number:]).span()[0] + index_begin_number
        return text[index_begin_number: index_end_number]


class ApartmentFloorHandler(AbstractHandler):
    def get_info(self, soup: bs4.BeautifulSoup) -> str or None:
        text = soup.text
        index_begin_number, index_end_number = re.search(r"[\d]+/", text).span()
        return text[index_begin_number: index_end_number-1]

class PriceHandler(AbstractHandler):
    def get_info(self, soup: bs4.BeautifulSoup) -> str or None:
        price_meta = soup.find("span", {"itemprop": "price"})
        price = price_meta.get("content")
        return price


class Distributor:
    def __init__(self, key: str):
        self.key = key

    def distribute(self) -> AbstractHandler:
        if self.key == "physical address":
            return PhysAddressHandler()
        elif self.key == "number of rooms":
            return AboutApartmentBlockHandler("Количество комнат")
        elif self.key == "area of apartment":
            return AboutApartmentBlockHandler("Общая площадь")
        elif self.key == "number of floors":
            return NFloorsHandler()
        elif self.key == "apartment floor":
            return ApartmentFloorHandler()
        elif self.key == "price":
            return PriceHandler()
        elif self.key == "repair":
            return AboutApartmentBlockHandler("Ремонт")
        elif self.key == "bathroom":
            return AboutApartmentBlockHandler("Санузел")
        elif self.key == "view from the windows":
            return AboutApartmentBlockHandler("Окна")
        elif self.key == "terrace":
            return AboutApartmentBlockHandler("Балкон или лоджия")
        elif self.key == "year of construction":
            return AboutHouseBlockHandler("Год постройки")
        elif self.key == "elevator":
            return AboutHouseBlockHandler("Пассажирский лифт")
        elif self.key == "extra":
            return AboutHouseBlockHandler("В доме")
        elif self.key == "type of house":
            return AboutApartmentBlockHandler("Тип дома")
        elif self.key == "parking":
            return AboutApartmentBlockHandler("Парковка")
        else:
            print("Встречен параметр, у которого отсутствует обработчик, параметр:", self.key)
            return EmptyHandler()