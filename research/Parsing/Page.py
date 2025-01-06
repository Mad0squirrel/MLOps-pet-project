"""Module for extracting the data from the page of listings."""

import random
import time

import bs4
import requests

from parsing.Post import Post


class Page:
    
    """Represent a single page of listings on the Avito website.

    Attributes
    ----------
    url : str
        The base URL of the page.
    p_num : int
        The current page number.
    session : requests.Session
        The session used for making HTTP requests.
    headers : dict
        The headers used for making HTTP requests.
    proxies : dict
        The proxies used for making HTTP requests.

    Methods
    -------
    get_urls() -> list
        Retrieves the URLs of listings from the current page.
    get_data(params: dict) -> list
        Retrieves the data for all listings on the current page using the provided parameters.
        
    """
    
    LOOP_DELAY = 3

    def __init__(self, url, page_number, session, headers, proxies):
        """Initialize the Page object with the necessary details."""
        self.url = url
        self.p_num = page_number
        self.session = session
        self.headers = headers
        self.proxies = proxies

    def get_urls(self) -> list:
        """Retrieve the URLs of listings from the current page.

        Sends an HTTP GET request to the specified page and parses the HTML 
        to extract the URLs of individual listings.

        Returns
        -------
        list
            A list of URLs for the listings on the current page.
            
        """
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
        """Retrieve the data for all listings on the current page.

        For each listing URL obtained from `get_urls`, this method creates a 
        `Post` object to extract data and returns the combined results.

        Parameters
        ----------
        params : dict
            The parameters used for data extraction in the Post object.

        Returns
        -------
        list
            A list of extracted data for the listings on the current page.
            
        """
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