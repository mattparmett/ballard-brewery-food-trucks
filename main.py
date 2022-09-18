import datetime
import pytz

import requests
from bs4 import BeautifulSoup
from icalendar import Calendar as iCalendar


def get_truck(url, parse_func):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
    }
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")
    return parse_func(soup)


def parse_obec(soup):
    header_elements = soup.select('span.btIconWidgetTitle')
    for element in header_elements:
        if (element.text != "Find our beer" and
                "hours" not in element.text.lower() and
                element.text != "No food truck scheduled today"):
            return element.text.replace("FOOD TRUCK: ","")
    return ""
    # return FoodTruck(name=obec_truck_element.text.replace("FOOD TRUCK: ", ""))

def parse_urban_family(soup):
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

        return truck_name, truck_date, truck_hours
        # return FoodTruck(name=truck_name, date=truck_date, hours=truck_hours)

def parse_stoup(soup):
    truck_element = soup.select_one('div[class="days0 food-truck-day"] > div')
    truck_date = truck_element.select_one('h5').text
    truck_day = truck_element.select_one('h4').text
    truck_name = truck_element.contents[-1]
    truck_hours = truck_element.contents[-3]

    return truck_name, truck_date, truck_day, truck_hours
    # return FoodTruck(name=truck_name, date=truck_date, day=truck_day, hours=truck_hours)

def parse_fair_isle(soup):
    truck_element = soup.select_one('div[class="content content-alignment--left"]')
    truck_name = truck_element.find('h4').text
    truck_date = truck_element.find('span').text
    return truck_name, truck_date
    # return FoodTruck(name=truck_name, date=truck_date)

def parse_lucky_envelope(soup):
    cal = iCalendar.from_ical(str(soup))

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

        return truck_name, full_date, truck_day, truck_hours
    # return FoodTruck(name=truck_name, date=truck_date, day=truck_day, hours=truck_hours)


def parse_reubens(soup):
    trucks = soup.select('*[class="food-truck-schedule-item"]')
    today = datetime.date.today()
    today_date = f"{today.month}/{today.day}"

    for truck in trucks:
        truck_date = truck.select_one('div[class="food-truck-day-name"]').text.strip()
        if today_date not in truck_date:
            continue

        truck_name = truck.select_one('div.vendor').text.strip()

        return truck_name, truck_date
        # return FoodTruck(name=truck_name, date=truck_date)

# def get_yonder():
#     url = 'https://www.bbycballard.com/food-trucks-1-1'
#     page = requests.get(url, headers=headers)
#     soup = BeautifulSoup(page.content, "html.parser")
#
#     weeks = soup.select('tr.yui3-calendar-row')
#     for week in weeks:
#         days = week.select('td')
#         for day in days:
#             date = day.select_one('div.marker')
#             if not date:
#                 continue
#
#             day_num = day.select_one('div.marker-daynum').text.strip()
#             if day_num == '' or int(day_num) != datetime.datetime.today().day:
#                 continue
#
#             truck = day.select_one('li.item')
#             truck_name = truck.select_one('span.item-title').text
#             truck_hours = truck.select_one('span[class="item-time item-time--12hr"]').text
#             truck_day = day.select_one('div.marker-dayname').text
#
#             return truck_name, day_num, truck_day, truck_hours
#             # return FoodTruck(name=truck_name, date=day_num, day=truck_day, hours=truck_hours)
#
#     return None


breweries = {
    'obec': {
        'url': 'https://www.obecbrewing.com',
        'parser': parse_obec
    },
    'urban_family': {
        'url': 'https://urbanfamilybrewing.com/food-trucks/',
        'parser': parse_urban_family
    },
    'stoup': {
        'url': 'https://www.stoupbrewing.com/ballard/#section-1379',
        'parser': parse_stoup
    },
    'fair isle': {
        'url': 'https://fairislebrewing.com/events/',
        'parser': parse_fair_isle
    },
    'lucky envelope': {
        'url': 'https://calendar.google.com/calendar/ical/luckyenvelopebrewing@gmail.com/public/basic.ics',
        'parser': parse_lucky_envelope
    },
    'reuben\'s': {
        'url': 'https://reubensbrews.com/visit-us/#food-trucks',
        'parser': parse_reubens
    },
}

if __name__ == '__main__':
    for brewery in breweries.values():
        print(get_truck(brewery['url'], brewery['parser']))

