import datetime
from typing import Optional

import pytz
from bs4 import BeautifulSoup
from icalendar import Calendar
from brewery import Brewery
from food_truck import FoodTruck


class LuckyEnvelope(Brewery):
    def __init__(self) -> None:
        super().__init__('Lucky Envelope', 'https://calendar.google.com/calendar/ical/luckyenvelopebrewing@gmail.com/public/basic.ics')

    def parse(self) -> Optional[FoodTruck]:
        soup: BeautifulSoup = self.make_request()
        cal: Calendar = Calendar.from_ical(str(soup))

        for component in cal.walk():
            try:
                truck_start_time: datetime = component['dtstart'].dt.astimezone(tz=pytz.timezone('US/Pacific'))
                truck_end_time: datetime = component['dtend'].dt.astimezone(tz=pytz.timezone('US/Pacific'))
                truck_name: str = component['summary'].to_ical().decode()
            except KeyError:
                continue

            today: datetime = datetime.date.today()
            # today: datetime = datetime.datetime.strptime('09/23/2022', '%m/%d/%Y').date()
            if not truck_start_time.date() == today:
                continue

            full_date: str = truck_start_time.strftime('%m/%d/%Y')
            truck_hours: str = f"{truck_start_time.strftime('%I%p')} - {truck_end_time.strftime('%I%p')}"

            return FoodTruck(truck_name, full_date, truck_hours)

        return None
