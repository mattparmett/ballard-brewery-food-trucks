from typing import Optional, List
import datetime

from bs4 import BeautifulSoup, element
from brewery import Brewery
from food_truck import FoodTruck

class Reubens(Brewery):
    def __init__(self) -> None:
        super().__init__('Reuben\'s', 'https://reubensbrews.com/visit-us/#food-trucks')

    def parse(self) -> Optional[FoodTruck]:
        soup: BeautifulSoup = self.make_request()
        trucks: List[element] = soup.select('*[class="food-truck-schedule-item"]')
        today: datetime = datetime.date.today()
        today_date: str = f"{today.month}/{today.day}"

        for truck in trucks:
            truck_date: str = truck.select_one('div[class="food-truck-day-name"]').text.strip()
            if today_date not in truck_date:
                continue

            truck_name: str = truck.select_one('div.vendor').text.strip()

            return FoodTruck(truck_name, truck_date, '')

        return None
