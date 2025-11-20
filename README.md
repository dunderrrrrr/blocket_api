<p align="center">
  <img src="https://blocket-api.se/blocket-api.png" />
</p>

# BlocketAPI

[![PyPI version](https://img.shields.io/pypi/v/blocket_api?style=for-the-badge)](https://pypi.org/project/blocket_api/) [![License](https://img.shields.io/badge/license-WTFPL-green?style=for-the-badge)](https://github.com/dunderrrrrr/blocket_api/blob/main/LICENSE) ![Python](https://img.shields.io/badge/Python-3.10-blue?style=for-the-badge) ![PyPI - Downloads](https://img.shields.io/pypi/dw/blocket_api?style=for-the-badge&color=%23dbce58) 

BlocketAPI allows users to search [blocket.se](https://blocket.se/) for ads.

> Blocket is one of Sweden's largest online marketplaces. It was founded in 1996 and allows users to buy and sell a wide range of items, including cars, real estate, jobs, services, and second-hand goods. The platform is known for its extensive reach and user-friendly interface, making it a popular choice for Swedes looking to purchase or sell items quickly and efficiently.

> [!NOTE]  
> Blocket recently released a new version of their site which caused this package to break. But do not fear, we are actively working to try and restore all functionality. More info in [issue #43](https://github.com/dunderrrrrr/blocket_api/issues/41).

## 🧑‍💻️ Install

Install BlocketAPI via PyPI...

```sh
pip install blocket-api
```

or use [blocket-api.se](https://blocket-api.se) without installing anything!

## 💁‍♀️ Usage

```py
from blocket_api import BlocketAPI, Category, Location, SortOrder

api = BlocketAPI()

result = api.search(
    "Vinterdäck Audi",
    sort_order=SortOrder.PRICE_ASC,
    locations=[Location.STOCKHOLM, Location.UPPSALA],
    category=Category.FORDONSTILLBEHOR,
)
```

## 📝 Notes

- REST API: https://blocket-api.se
- Source repo: https://github.com/dunderrrrrr/blocket_api
- PyPI: https://pypi.org/project/blocket-api/
