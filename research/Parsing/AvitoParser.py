# AvitoParser.py
import csv
import time
import json
import requests
import bs4
import random
from research.Parsing.Page import Page



class AvitoParser:
    LOOP_DELAY = 20

    def __init__(self):
        self.url = None
        self.file_name = None
        self.cookies = None
        self.headers = None
        self.params = None
        self.proxies = None
        self.has_headers = True
        self.load_new_configs()
        self.session = requests.Session()



    def get_n_pages(self) -> int or None:
        try:
            request = self.session.get(self.url, headers=self.headers, proxies=self.proxies)
            if request.status_code != 200:
                print(f"Ошибка при загрузке страницы. Статус: {request.status_code}")
                return None
            html = request.text
            soup = bs4.BeautifulSoup(html, "lxml")
            list_page_buttons = soup.select_one("div.js-pages.pagination-pagination-Oz4Ri").select('span')
            # page_numbers = []
            # for button in list_page_buttons:
            #     try:
            #         page_numbers.append(int(button.text))
            #     except ValueError:
            #         continue

            # if not page_numbers:
            #     print("Номера страниц не найдены")
            #     return None

            # return max(page_numbers)
            return 3
        except requests.exceptions.ConnectionError:
            print("Отсутствует соединение")
            return None

    def save_data(self, data: list) -> None:
        print("Сохранение")
        if not self.has_headers:
            headers = [key for key in self.params if self.params[key]]
            with open(self.file_name, 'w', newline='', encoding='utf-8') as csv_file:
                writer = csv.writer(csv_file, delimiter=';')
                writer.writerow(headers)
            self.has_headers = True

        with open(self.file_name, 'a', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file, delimiter=';')
            writer.writerows(data)

    def load_new_configs(self) -> None:
        try:
            with open("research/Parsing/configs.json", 'r') as read_f:
                configs = json.load(read_f)
            self.url = configs['url']
            self.file_name = configs['file_name']
            self.cookies = configs['cookies']
            self.headers = configs['headers']
            self.params = configs['params']
            self.proxies = configs['proxies']
        except FileNotFoundError:
            print("Отсутствует файл configs.json")

    def start(self) -> None:
        n_pages = self.get_n_pages()
        print(f"Количество страниц: {n_pages}")
        if not n_pages:
            print("Ошибка: количество страниц не определено.")
            return

        for number_page in range(1, n_pages + 1):
            print(f"Парсинг страницы {number_page} из {n_pages}")
            page = Page(self.url, number_page, self.session, self.headers, self.proxies)
            data = page.get_data(self.params)
            if not data:
                print(f"Ошибка при получении данных для страницы {number_page}. Останавливаю парсинг.")
                return
            self.save_data(data)
            delay = AvitoParser.LOOP_DELAY + random.uniform(1, 5)  # Случайная задержка для имитации активности человека
            time.sleep(delay)
