import datetime

from bs4 import BeautifulSoup
from brewery import Brewery
from food_truck import FoodTruck

class Reubens(Brewery):
    def __init__(self):
        super().__init__('Reuben\'s', 'https://reubensbrews.com/visit-us/#food-trucks')

    def parse(self) -> FoodTruck | None:
        soup = self.make_request()
        trucks = soup.select('*[class="food-truck-schedule-item"]')
        today = datetime.date.today()
        today_date = f"{today.month}/{today.day}"

        for truck in trucks:
            truck_date = truck.select_one('div[class="food-truck-day-name"]').text.strip()
            if today_date not in truck_date:
                continue

            truck_name = truck.select_one('div.vendor').text.strip()

            return FoodTruck(truck_name, truck_date, '')

        return None
