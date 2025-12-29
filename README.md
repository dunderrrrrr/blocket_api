<p align="center">
  <img src="https://blocket-api.se/blocket-api.png" />
</p>

# BlocketAPI

[![PyPI version](https://img.shields.io/pypi/v/blocket_api?style=for-the-badge)](https://pypi.org/project/blocket_api/) [![License](https://img.shields.io/badge/license-WTFPL-green?style=for-the-badge)](https://github.com/dunderrrrrr/blocket_api/blob/main/LICENSE) ![Python](https://img.shields.io/badge/Python-3.10-blue?style=for-the-badge) ![PyPI - Downloads](https://img.shields.io/pypi/dw/blocket_api?style=for-the-badge&color=%23dbce58) 

BlocketAPI allows users to search [blocket.se](https://blocket.se/) for ads.

> Blocket is one of Sweden's largest online marketplaces. It was founded in 1996 and allows users to buy and sell a wide range of items, including cars, real estate, jobs, services, and second-hand goods. The platform is known for its extensive reach and user-friendly interface, making it a popular choice for Swedes looking to purchase or sell items quickly and efficiently.

## 🧑‍💻️ Install

Install BlocketAPI via PyPI...

```sh
pip install blocket-api
```

or use [blocket-api.se](https://blocket-api.se) without installing anything!

## 💁‍♀️ Usage

```py
from blocket_api import (
    BlocketAPI,
    Category,
    CarColor,
    CarModel,
    CarSortOrder,
    CarTransmission,
    Location,
)

api = BlocketAPI()

# search all of blocket
api.search(
    "Tamagotchi",
    sort_order=SortOrder.PRICE_ASC,
    locations=[Location.STOCKHOLM, Location.UPPSALA],
    category=Category.FRITID_HOBBY_OCH_UNDERHALLNING,
)

# search for cars
api.search_car(
    "Audi", # query is optional
    sort_order=CarSortOrder.MILEAGE_ASC,
    models=[CarModel.AUDI],
    colors=[CarColor.GULD],
    price_from=10000,
    price_to=50000,
    transmissions=[CarTransmission.MANUAL],
    locations=[Location.STOCKHOLM],
    org_id=1337, # dealer or store id
)

# search for boats
from blocket_api import BoatType

api.search_boat(
    "Mercury", # query is optional
    types=[BoatType.DAYCRUISER],
    locations=[Location.STOCKHOLM],
    length_from=10,
    length_to=15,    
    price_from=20000,
    price_to=90000,
    org_id=1337, # dealer or store id
)

# search for motorcycles
from blocket_api import McType, McModel

api.search_mc(
    "TC 150", # query is optional
    types=[McType.SPORT],
    locations=[Location.STOCKHOLM],
    models=[McModel.DUCATI],
    price_from=20000,
    price_to=90000,
    engine_volume_from=100,
    engine_volume_to=200,
    org_id=1337, # dealer or store id
)


# get ad details
from blocket_api import CarAd, RecommerceAd, BoatAd, McAd

api.get_ad(RecommerceAd(12345678))
api.get_ad(CarAd(12345678))
api.get_ad(BoatAd(12345678))
api.get_ad(McAd(12345678))
```

## 📝 Notes

- REST API: https://blocket-api.se
- Source repo: https://github.com/dunderrrrrr/blocket_api
- PyPI: https://pypi.org/project/blocket-api/
