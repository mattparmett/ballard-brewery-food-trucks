from breweries import *

if __name__ == '__main__':
    breweries = [
        FairIsle(),
        LuckyEnvelope(),
        Obec(),
        Reubens(),
        Stoup(),
        UrbanFamily(),
        # Yonder(),
    ]

    for brewery in breweries:
        print(brewery.name, brewery.parse())
