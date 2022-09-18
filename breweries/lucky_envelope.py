import datetime

import pytz
from bs4 import BeautifulSoup
from icalendar import Calendar
from brewery import Brewery
from food_truck import FoodTruck

class LuckyEnvelope(Brewery):
    def __init__(self):
        super().__init__('Lucky Envelope', 'https://calendar.google.com/calendar/ical/luckyenvelopebrewing@gmail.com/public/basic.ics')

    def parse(self) -> FoodTruck | None:
        soup = self.make_request()
        cal = Calendar.from_ical(str(soup))

        for component in cal.walk():
            try:
                truck_start_time = component['dtstart'].dt.astimezone(tz=pytz.timezone('US/Pacific'))
                truck_end_time = component['dtend'].dt.astimezone(tz=pytz.timezone('US/Pacific'))
                truck_name = component['summary'].to_ical().decode()
            except KeyError:
                continue

            today = datetime.date.today()
            # today = datetime.datetime.strptime('09/23/2022', '%m/%d/%Y').date()
            if not truck_start_time.date() == today:
                continue

            full_date = truck_start_time.strftime('%m/%d/%Y')
            truck_day = truck_start_time.strftime('%A')
            truck_hours = f"{truck_start_time.strftime('%I%p')} - {truck_end_time.strftime('%I%p')}"

            return FoodTruck(truck_name, full_date, truck_hours)

        return None
