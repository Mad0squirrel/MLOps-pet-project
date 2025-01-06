"""Module for extracting data from an individual listing post."""
from bs4 import BeautifulSoup

from parsing.Handler import Distributor


class Post:
    
    """Represent an individual listing post on the Avito website.

    This class is responsible for retrieving the detailed information 
    of a specific listing by using the provided short URL, making an 
    HTTP request to fetch the page, parsing the HTML response, and 
    extracting data based on the specified parameters.

    Attributes
    ----------
    domain : str
        The base URL of the Avito website.
    short_url : str
        The short URL of the specific listing.
    session : requests.Session
        The session used to make HTTP requests.
    headers : dict
        The headers to be used for HTTP requests.
    proxies : dict
        The proxies to be used for HTTP requests, if necessary.

    Methods
    -------
    get_data(params: dict) -> list
        Fetches the listing data based on the provided parameters, 
        parses the page content, and returns the extracted values.
        
    """
    
    domain = "https://www.avito.ru"

    def __init__(self, short_url, session, headers, proxies):
        """Initialize the Post object."""
        self.short_url = short_url
        self.session = session
        self.headers = headers
        self.proxies = proxies

    def get_data(self, params: dict) -> list:
        """Fetch and extract data from a single listing post.

        This method makes an HTTP request to the full URL of the post, 
        parses the HTML response using BeautifulSoup, and then extracts 
        the requested data based on the provided parameters. It uses 
        the Distributor to delegate the extraction to the appropriate handler 
        for each parameter.

        Parameters
        ----------
        params : dict
            A dictionary where the keys are data fields to be extracted (e.g., "price", "area"), 
            and the values are booleans indicating whether the data for that field should be fetched.

        Returns
        -------
        list
            A list of extracted values corresponding to the parameters in `params`.
            If a parameter's value is not available or an error occurs, `None` is returned for that field.
            
        """
        full_url = Post.domain + self.short_url
        request = self.session.get(full_url, headers=self.headers, proxies=self.proxies)
        print(full_url)
        if request.reason != 'OK':
            print("Возникла ошибка", request.reason)
        html = request.text
        soup = BeautifulSoup(html, "lxml")
        key_storage = dict()
        for key in [key for key in params if params[key]]:
            if key == "link":
                key_storage[key] = full_url
            else:
                handler = Distributor(key).distribute()
                try:
                    key_storage[key] = handler.get_info(soup)
                except (AttributeError, TypeError):
                    key_storage[key] = None
        return list(key_storage.values())


