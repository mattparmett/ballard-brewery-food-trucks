import datetime

from brewery import Brewery
from food_truck import FoodTruck

class Yonder(Brewery):
    def __init__(self):
        super().__init__('Yonder', 'https://www.bbycballard.com/food-trucks-1-1')

    def parse(self) -> FoodTruck | None:
        soup = self.make_request()
        weeks = soup.select('tr.yui3-calendar-row')
        for week in weeks:
            days = week.select('td')
            for day in days:
                date = day.select_one('div.marker')
                if not date:
                    continue

                day_num = day.select_one('div.marker-daynum').text.strip()
                if day_num == '' or int(day_num) != datetime.datetime.today().day:
                    continue

                truck = day.select_one('li.item')
                truck_name = truck.select_one('span.item-title').text
                truck_hours = truck.select_one('span[class="item-time item-time--12hr"]').text
                # truck_day = day.select_one('div.marker-dayname').text

                return FoodTruck(truck_name, day_num, truck_hours)

        return None
