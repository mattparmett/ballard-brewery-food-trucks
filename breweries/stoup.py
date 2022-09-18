from typing import Optional

from bs4 import BeautifulSoup, element
from brewery import Brewery
from food_truck import FoodTruck

class Stoup(Brewery):
    def __init__(self) -> None:
        super().__init__('Stoup', 'https://www.stoupbrewing.com/ballard/#section-1379')

    def parse(self) -> Optional[FoodTruck]:
        soup: BeautifulSoup = self.make_request()
        truck_element: element = soup.select_one('div[class="days0 food-truck-day"] > div')
        truck_date: str = truck_element.select_one('h5').text
        truck_name: str = truck_element.contents[-1].text
        truck_hours: str = truck_element.contents[-3].text

        return FoodTruck(truck_name, truck_date, truck_hours)