import datetime
import json
import os.path
from typing import Optional

from flask import Flask
from breweries import *
from brewery import Brewery

app = Flask(__name__)
CACHE_PATH: str = os.path.abspath('cache.txt')


@app.route("/")
def home() -> str:
    trucks: dict[str, Optional[str]] = {}
    if cache_warm():
        try:
            trucks.update(parse_cache())
        except OSError:
            pass

    if not trucks:
        trucks = scrape_trucks()

    today: str = datetime.date.today().strftime('%A, %B %d, %Y')
    heading: str = f"<h1>Ballard Brewery Food Trucks for {today}:</h1>"
    truck_output: str = '\n'.join([
        f"<p><strong>{brewery_name}</strong>: {truck or 'No food truck today.'}</p>"
        for brewery_name, truck
        in trucks.items()
    ])

    return f"<html><body>{heading}{truck_output}</body></html>"


def cache_warm(cache_path: str = None):
    if cache_path is None:
        cache_path = CACHE_PATH

    try:
        cache_modified_time: float = os.path.getmtime(cache_path)
    except OSError:
        return False

    cache_modified_date: datetime.date = datetime.date.fromtimestamp(cache_modified_time)
    return cache_modified_date == datetime.date.today()


def parse_cache(cache_path: str = None) -> dict[str, Optional[str]]:
    if cache_path is None:
        cache_path = CACHE_PATH

    with open(cache_path, 'r') as cache_file:
        return json.loads(cache_file.read())


def write_cache(contents: dict[str, Optional[str]], cache_path: str = None) -> None:
    if cache_path is None:
        cache_path = CACHE_PATH

    with open(cache_path, 'w') as cache_file:
        json.dump(contents, cache_file)


def scrape_trucks() -> dict[str, Optional[str]]:
    breweries: list[Brewery] = [
        FairIsle(),
        LuckyEnvelope(),
        Obec(),
        Reubens(),
        Stoup(),
        UrbanFamily(),
        # Yonder(),
    ]

    trucks: dict[str, Optional[str]] = {brewery.name: str(brewery.parse()) for brewery in breweries}

    try:
        write_cache(trucks)
    except OSError:
        pass

    return trucks


