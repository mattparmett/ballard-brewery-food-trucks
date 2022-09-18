from bs4 import BeautifulSoup
from brewery import Brewery
from food_truck import FoodTruck

class Stoup(Brewery):
    def __init__(self):
        super().__init__('Stoup', 'https://www.stoupbrewing.com/ballard/#section-1379')

    def parse(self) -> FoodTruck | None:
        soup = self.make_request()
        truck_element = soup.select_one('div[class="days0 food-truck-day"] > div')
        truck_date = truck_element.select_one('h5').text
        # truck_day = truck_element.select_one('h4').text
        truck_name = truck_element.contents[-1].text
        truck_hours = truck_element.contents[-3].text

        return FoodTruck(truck_name, truck_date, truck_hours)