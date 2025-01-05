"""Module for handling and extracting specific information from HTML content.

This module implements a set of handlers based on the AbstractHandler class, 
each designed to extract particular types of data (e.g., price, address, number of floors) 
from parsed HTML content using BeautifulSoup. A distributor class is also provided 
to dynamically assign the appropriate handler based on the type of data required.

Classes
-------
AbstractHandler (ABC)
    An abstract base class defining the interface for all handlers.
AboutApartmentBlockHandler(AbstractHandler)
    Extracts apartment-related information (e.g., area, repair, type of house).
AboutHouseBlockHandler(AbstractHandler)
    Extracts house-related information (e.g., year of construction, elevator).
PhysAddressHandler(AbstractHandler)
    Extracts the physical address of the property.
PriceHandler(AbstractHandler)
    Extracts the price of the property.
NFloorsHandler(AbstractHandler)
    Extracts the total number of floors in the building.
ApartmentFloorHandler(AbstractHandler)
    Extracts the floor number of the apartment.
EmptyHandler(AbstractHandler)
    A placeholder handler that always returns None.
Distributor
    A class that selects and returns the appropriate handler based on a given key.

Usage
-----
1. Instantiate the `Distributor` class with a specific key (e.g., "price", "physical address").
2. Call the `distribute` method to get the appropriate handler.
3. Use the handler's `get_info` method to extract the desired information from a BeautifulSoup object.

"""

import re
from abc import ABC, abstractmethod

import bs4


class AbstractHandler(ABC):

    """Abstract base class for handlers that extract specific information from a BeautifulSoup object.

    Methods
    -------
    get_info(soup: bs4.BeautifulSoup) -> str or None
        Abstract method to extract information from the provided BeautifulSoup object.

    """

    @abstractmethod
    def get_info(self, soup: bs4.BeautifulSoup) -> str | None:
        """Extract information from the provided BeautifulSoup object.

        Parameters
        ----------
        soup : bs4.BeautifulSoup
            Parsed HTML data.

        Returns
        -------
        str or None
            Extracted information or None if extraction fails.
            
        """
        pass


class AboutApartmentBlockHandler(AbstractHandler):

    """Handler for extracting information about an apartment block (e.g., number of rooms, area).

    Attributes
    ----------
    key_word : str
        The keyword used to locate the desired information.

    Methods
    -------
    get_info(soup: bs4.BeautifulSoup) -> str or None
        Extracts information from the apartment block section.
        
    """
        
    def __init__(self, key_word):
        """Initialize the handler with a specific keyword.

        Parameters
        ----------
        key_word : str
            The keyword to search for in the HTML.
            
        """
        self.key_word: str = key_word

    def get_info(self, soup: bs4.BeautifulSoup) -> str | None:
        """Extract data from the provided BeautifulSoup object."""
        items = soup.select('ul.params-paramsList-_awNW > li')
        for item in items:
            key = item.find('span', class_='styles-module-noAccent-l9CMS')
            if key and self.key_word in key.text:
                full_text = item.get_text(separator=" ", strip=True)
                cleaned_value = full_text.replace(self.key_word, "").removesuffix(" : ")
                return cleaned_value
        return None


class AboutHouseBlockHandler(AbstractHandler):
    
    """Handler for extracting information about a house block (e.g., year of construction, elevator).

    Attributes
    ----------
    key_word : str
        The keyword used to locate the desired information.

    Methods
    -------
    get_info(soup: bs4.BeautifulSoup) -> str or None
        Extracts information from the house block section.
        
    """
    
    def __init__(self, key_word):
        """Initialize the handler with a specific keyword.

        Parameters
        ----------
        key_word : str
            The keyword to search for in the HTML.
            
        """
        self.key_word: str = key_word

    def get_info(self, soup: bs4.BeautifulSoup) -> str | None:
        """Extract data from the provided BeautifulSoup object."""
        items = soup.select('ul.params-paramsList-_awNW > li')
        for item in items:
            key = item.find('span', class_='styles-module-noAccent-l9CMS')
            if key and self.key_word in key.text:
                full_text = item.get_text(separator=" ", strip=True)
                cleaned_value = full_text.replace(self.key_word, "").removesuffix(" : ")
                return cleaned_value
        return None


class EmptyHandler(AbstractHandler):

    """Handler that returns None for unsupported or unknown keys.

    Methods
    -------
    get_info(soup: bs4.BeautifulSoup) -> None
        Always returns None.
        
    """

    def get_info(self, soup: bs4.BeautifulSoup) -> str | None:
        """Abstract method for extracting specific information from a BeautifulSoup object."""
        return None


class PhysAddressHandler(AbstractHandler):
    
    """Handler for extracting the physical address from the HTML.

    Methods
    -------
    get_info(soup: bs4.BeautifulSoup) -> str or None
        Extracts the physical address.
        
    """
    
    def get_info(self, soup: bs4.BeautifulSoup) -> str | None:
        """Extract the physical address from the provided BeautifulSoup object."""
        geo_block = soup.select_one("span.style-item-address__string-wt61A")
        address = geo_block.text.strip().replace("\n", "|")
        return address


class NFloorsHandler(AbstractHandler):
    
    """Handler for extracting the total number of floors in a building.

    Methods
    -------
    get_info(soup: bs4.BeautifulSoup) -> str or None
        Extracts the total number of floors.
        
    """
    
    def get_info(self, soup: bs4.BeautifulSoup) -> str | None:
        """Extract the number of floors from the provided BeautifulSoup object."""
        text = soup.text
        index_begin_number = re.search("/", text).span()[1]
        index_end_number = re.search(" ", text[index_begin_number:]).span()[0] + index_begin_number
        return text[index_begin_number: index_end_number]


class ApartmentFloorHandler(AbstractHandler):
    
    """Handler for extracting the apartment's floor number.

    Methods
    -------
    get_info(soup: bs4.BeautifulSoup) -> str or None
        Extracts the apartment's floor number.
        
    """
    
    def get_info(self, soup: bs4.BeautifulSoup) -> str | None:
        """Extract the apartment's floor number from the provided BeautifulSoup object."""
        text = soup.text
        index_begin_number, index_end_number = re.search(r"[\d]+/", text).span()
        return text[index_begin_number: index_end_number-1]

class PriceHandler(AbstractHandler):
    
    """Handler for extracting the price of the real estate item.

    Methods
    -------
    get_info(soup: bs4.BeautifulSoup) -> str or None
        Extracts the price.
        
    """
    
    def get_info(self, soup: bs4.BeautifulSoup) -> str | None:
        """Extract the price of the real estate from the provided BeautifulSoup object."""
        price_meta = soup.find("span", {"itemprop": "price"})
        price = price_meta.get("content")
        return price


class Distributor:
    
    """Distribute the appropriate handler based on the provided key.

    Attributes
    ----------
    key : str
        The name of the parameter to extract.

    Methods
    -------
    distribute() -> AbstractHandler
        Returns the appropriate handler for the given key.
        
    """
    
    def __init__(self, key: str):
        """Initialize the Distributor with the given key."""
        self.key = key

    def distribute(self) -> AbstractHandler:
        """Return the appropriate handler based on the key.

        Returns
        -------
        AbstractHandler
            The handler responsible for extracting the parameter.
            
        """
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