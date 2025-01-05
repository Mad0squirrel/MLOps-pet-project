"""Module for parsing advertisements from the Avito website.

This module implements the `AvitoParser` class, which is responsible for:
- Retrieving the number of pages for a specific category or theme.
- Collecting data from each page.
- Saving the data to a CSV file.

Settings such as URL, headers, parameters, and proxies are loaded from the `configs.json` file.
"""

import csv
import json
import random
import time

import bs4
import requests

from Parsing.Page import Page


class AvitoParser:

    """Parser of real estate data from the Avito website.

    Attributes
    ----------
    url : str or None
        The URL for parsing.
    file_name : str or None
        The name of the file to save parsed data.
    headers : dict or None
        The headers for HTTP requests.
    params : dict or None
        The parameters for data filtering or processing.
    proxies : dict or None
        Proxy settings for HTTP requests.
    has_headers : bool
        Indicates if the headers have already been written to the output file.
    session : requests.Session
        HTTP session to reuse connections.

    Methods
    -------
    get_n_pages() -> int or None
        Retrieves the number of pages for the given URL.
    save_data(data: list) -> None
        Saves parsed data to a CSV file.
    load_new_configs() -> None
        Loads configuration settings from a JSON file.
    start() -> None
        Starts the parsing process.

    """

    LOOP_DELAY = 3

    def __init__(self):
        """Initialize a parser."""
        self.url: str | None = None
        self.file_name: str | None = None
        self.headers: dict | None = None
        self.params: dict | None = None
        self.proxies: dict | None = None
        self.has_headers: bool = False
        self.load_new_configs()
        self.session: requests.Session = requests.Session()



    def get_n_pages(self) -> int | None:
        """Determine the number of pages available for the given URL.

        Returns
        -------
        int or None
        The maximum page number if found, otherwise None in case of errors.

        """
        try:
            request = self.session.get(self.url, headers=self.headers, proxies=self.proxies)
            if request.status_code != 200:
                print(f"Ошибка при загрузке страницы. Статус: {request.status_code}")
                return None
            html = request.text
            soup = bs4.BeautifulSoup(html, "lxml")
            list_page_buttons = soup.select_one("div.js-pages.pagination-pagination-Oz4Ri").select('span')
            page_numbers = []
            for button in list_page_buttons:
                try:
                    page_numbers.append(int(button.text))
                except ValueError:
                    continue

            if not page_numbers:
                print("Номера страниц не найдены")
                return None

            return max(page_numbers)
        except requests.exceptions.ConnectionError:
            print("Отсутствует соединение")
            return None

    def save_data(self, data: list) -> None:
        """Save the parsed data into a CSV file.

        Parameters
        ----------
        data : list
            A list of rows (each row is a list) to be written into the file.

        """
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
        """Load configuration settings from a JSON file.

        The settings include URL, headers, parameters, and proxy information.
        If the file is missing or contains errors, an appropriate message is displayed.
        """
        try:
            with open("Parsing/configs.json", 'r') as read_f:
                configs = json.load(read_f)
            self.url = configs['url']
            self.file_name = configs['file_name']
            self.headers = configs['headers']
            self.params = configs['params']
            self.proxies = configs['proxies']
        except FileNotFoundError:
            print("Отсутствует файл configs.json")

    def start(self) -> None:
        """Initiate the parsing process.

        The method retrieves the number of pages, iterates through each page,
        extracts data, and saves it to a CSV file. Includes delay between requests
        to prevent potential blocking by the website.
        """
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
            delay = AvitoParser.LOOP_DELAY + random.uniform(1, 4)
            time.sleep(delay)
