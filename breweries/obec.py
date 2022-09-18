from bs4 import BeautifulSoup
from brewery import Brewery
from food_truck import FoodTruck

class Obec(Brewery):
    def __init__(self):
        super().__init__('Obec', 'https://www.obecbrewing.com')

    def parse(self) -> FoodTruck | None:
        soup = self.make_request()
        header_elements = soup.select('span.btIconWidgetTitle')
        for element in header_elements:
            if (element.text != "Find our beer" and
                    "hours" not in element.text.lower() and
                    element.text != "No food truck scheduled today"):
                return FoodTruck(element.text.replace("FOOD TRUCK: ", ""))
        return None
