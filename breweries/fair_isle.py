from brewery import Brewery
from food_truck import FoodTruck

class FairIsle(Brewery):
    def __init__(self):
        super().__init__('Fair Isle', 'https://fairislebrewing.com/events/')

    def parse(self) -> FoodTruck | None:
        soup = self.make_request()
        truck_element = soup.select_one('div[class="content content-alignment--left"]')
        truck_name = truck_element.find('h4').text
        truck_date = truck_element.find('span').text
        return FoodTruck(truck_name, truck_date, '')
