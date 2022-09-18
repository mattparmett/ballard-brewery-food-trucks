from abc import ABC, abstractmethod
from typing import Optional

import requests
from bs4 import BeautifulSoup
from food_truck import FoodTruck


class Brewery(ABC):
    """
    Represents a brewery; stores the brewery's name and url,
    which should point to the food truck page on the brewery's
    website.

    Every implementation of Brewery should define a parse method
    that parses the contents of the Brewery's food truck page
    and returns a FoodTruck object.
    """
    def __init__(self, name: str, url: str) -> None:
        self.name = name
        self.url = url

    def make_request(self) -> BeautifulSoup:
        headers: dict[str, str] = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
        }
        response: requests.Response = requests.get(self.url, headers=headers)
        return BeautifulSoup(response.content, "html.parser")

    @abstractmethod
    def parse(self) -> Optional[FoodTruck]:
        pass


    def __str__(self) -> str:
        return f"{self.name}: {self.url}"

    def __repr__(self) -> str:
        return str(self)
