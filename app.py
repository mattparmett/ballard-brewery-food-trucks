import datetime

from breweries import *
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    breweries = [
        FairIsle(),
        LuckyEnvelope(),
        Obec(),
        Reubens(),
        Stoup(),
        UrbanFamily(),
        # Yonder(),
    ]
    today = datetime.date.today().strftime('%A, %B %d, %Y')
    heading = f"<h1>Ballard Brewery Food Trucks for {today}:</h1>"
    return f"<html><body>{heading}" + '\n'.join([f"<p><strong>{brewery.name}</strong>: {brewery.parse()}</p>" for brewery in breweries]) + "</body></html>"
