from bs4 import BeautifulSoup
import bs4
import re
from abc import ABC, abstractmethod

# Пример HTML-документа
html = """
<ul class="params-paramsList__aawNh">
    <li class="params-paramsList__item-_2xYo">
        <span class="styles-module-noAccent-19CkMS">Количество комнат</span>
        <span>: </span>
        3
    </li>
</ul>
"""



# Инициализация BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

class AbstractHandler(ABC):
    @abstractmethod
    def get_info(self, soup: bs4.BeautifulSoup) -> str or None:
        pass

class AboutApartmentBlockHandler(AbstractHandler):
    def __init__(self, key_word):
        self.key_word = key_word

    def get_info(self, soup: bs4.BeautifulSoup) -> str or None:
        # Найти все элементы списка параметров
        items = soup.select('ul.params-paramsList__aawNh > li')
        for item in items:
            # Проверяем, содержит ли ключевой элемент текст ключевого слова
            key = item.find('span', class_='styles-module-noAccent-19CkMS')
            if key and self.key_word in key.text:
                # Убираем все вложенные теги и возвращаем оставшийся текст после ключевого слова
                text = item.get_text(separator=" ", strip=True)
                value = text.replace(self.key_word, "").strip(' : ')
                return value
        return None

# Использование класса
handler = AboutApartmentBlockHandler(key_word="Количество комнат")
info = handler.get_info(soup)
print(info)  # Вывод: "3"