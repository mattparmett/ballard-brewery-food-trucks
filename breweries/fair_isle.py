from typing import Optional

from bs4 import BeautifulSoup, element

from brewery import Brewery
from food_truck import FoodTruck


class FairIsle(Brewery):
    def __init__(self) -> None:
        super().__init__('Fair Isle', 'https://fairislebrewing.com/events/')

    def parse(self) -> Optional[FoodTruck]:
        soup: BeautifulSoup = self.make_request()
        truck_element: element = soup.select_one('div[class="content content-alignment--left"]')
        truck_name: str = truck_element.find('h4').text
        truck_date: str = truck_element.find('span').text
        return FoodTruck(truck_name, truck_date, '')
