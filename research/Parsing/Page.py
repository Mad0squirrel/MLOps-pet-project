import random
import time

import bs4
import requests

from Parsing.Post import Post


class Page:
    LOOP_DELAY = 3

    def __init__(self, url, page_number, session, headers, proxies):
        self.url = url
        self.p_num = page_number
        self.session = session
        self.headers = headers
        self.proxies = proxies

    def get_urls(self) -> list:
        try:
            request = self.session.get(self.url, params=dict(p=self.p_num), headers=self.headers, proxies=self.proxies)
            html = request.text
            soup = bs4.BeautifulSoup(html, "lxml")
            blocks = soup.select("div.iva-item-content-OWwoq")
            urls = []
            for block in blocks:
                url = block.select_one('div.iva-item-titleStep-zichc').select_one('a').get('href')
                urls.append(url)
            return urls
        except requests.exceptions.ConnectionError:
            print("Отсутствует соединение")
            return []

    def get_data(self, params: dict) -> list:
        urls = self.get_urls()
        data = []
        for url in urls:
            try:
                post = Post(url, self.session, self.headers, self.proxies)
                data.append(post.get_data(params))
                delay = Page.LOOP_DELAY + random.uniform(1, 4)
                time.sleep(delay)
            except requests.exceptions.ConnectionError:
                return data
        return data