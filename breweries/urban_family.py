import datetime

from bs4 import BeautifulSoup
from brewery import Brewery
from food_truck import FoodTruck

class UrbanFamily(Brewery):
    def __init__(self):
        super().__init__('Urban Family', 'https://urbanfamilybrewing.com/food-trucks/')

    def parse(self) -> FoodTruck | None:
        soup = self.make_request()
        days = soup.select('div[class="tribe-events-calendar-month__day"]')
        today = datetime.date.today().strftime('%Y-%m-%d')
        for day in days:
            truck_date = (day.select_one('time.tribe-events-calendar-month__day-date-daynum')
                             .attrs['datetime']
                             .strip())
            if today != truck_date:
                continue

            truck_hours = ''
            for time in day.select('div.tribe-events-calendar-month__calendar-event-datetime > time'):
                if truck_hours:
                    truck_hours += ' - '
                truck_hours += time.text.strip()

            truck_name = (day.select_one('h3[class="tribe-events-calendar-month__calendar-event-title tribe-common-h8 tribe-common-h--alt"]')
                             .text
                             .strip())

            return FoodTruck(truck_name, truck_date, truck_hours)

        return None
