from typing import Optional, List
from bs4 import BeautifulSoup, element
from brewery import Brewery
from food_truck import FoodTruck

class Obec(Brewery):
    def __init__(self) -> None:
        super().__init__('Obec', 'https://www.obecbrewing.com')

    def parse(self) -> Optional[FoodTruck]:
        soup: BeautifulSoup = self.make_request()
        header_elements: List[element] = soup.select('span.btIconWidgetTitle')
        for header_element in header_elements:
            if (header_element.text != "Find our beer" and
                    "hours" not in header_element.text.lower() and
                    header_element.text != "No food truck scheduled today"):
                return FoodTruck(header_element.text.replace("FOOD TRUCK: ", ""), '', '')
        return None
