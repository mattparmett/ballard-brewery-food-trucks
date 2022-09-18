import datetime
from typing import Optional, List

from bs4 import BeautifulSoup, element

from brewery import Brewery
from food_truck import FoodTruck

class Yonder(Brewery):
    def __init__(self) -> None:
        super().__init__('Yonder', 'https://www.bbycballard.com/food-trucks-1-1')

    def parse(self) -> Optional[FoodTruck]:
        soup: BeautifulSoup = self.make_request()
        weeks: List[element] = soup.select('tr.yui3-calendar-row')
        for week in weeks:
            days: element = week.select('td')
            for day in days:
                date: element = day.select_one('div.marker')
                if not date:
                    continue

                day_num: str = day.select_one('div.marker-daynum').text.strip()
                if day_num == '' or int(day_num) != datetime.datetime.today().day:
                    continue

                truck: element = day.select_one('li.item')
                truck_name: str = truck.select_one('span.item-title').text
                truck_hours: str = truck.select_one('span[class="item-time item-time--12hr"]').text

                return FoodTruck(truck_name, day_num, truck_hours)

        return None
