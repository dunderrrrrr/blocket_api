# BlocketAPI

[![PyPI version](https://img.shields.io/pypi/v/blocket_api?style=for-the-badge)](https://pypi.org/project/blocket_api/) [![License](https://img.shields.io/badge/license-WTFPL-green?style=for-the-badge)](https://github.com/dunderrrrrr/blocket_api/blob/main/LICENSE) [![Python versions](https://img.shields.io/pypi/pyversions/blocket-api?style=for-the-badge)](https://pypi.org/project/blocket_api/) ![PyPI - Downloads](https://img.shields.io/pypi/dm/blocket_api?style=for-the-badge&color=%23dbce58)

BlocketAPI allows users to query saved searches, known as "Bevakningar", on [blocket.se](https://blocket.se/). This means you can either retrieve results from a specific saved search or list all listings/ads across all saved searches. The results from these queries are returned in a `json` format.

> Blocket is one of Sweden's largest online marketplaces. It was founded in 1996 and allows users to buy and sell a wide range of items, including cars, real estate, jobs, services, and second-hand goods. The platform is known for its extensive reach and user-friendly interface, making it a popular choice for Swedes looking to purchase or sell items quickly and efficiently.

## ✨ Features

- List saved searches, called "Bevakningar".
- Query all listings/ads filtered on a region.
- Query listings related to a saved search.
- Use motor search to query listings related to a specific car.

## 🧑‍💻️ Install

BlocketAPI is available on PyPI.

```sh
pip install blocket-api
```

## 💁‍♀️ Usage

```py
>>> from blocket_api import BlocketAPI
>>> api = BlocketAPI("YourBlocketTokenHere")
>>> print(api.saved_searches())
...
>>> print(BlocketAPI().custom_search("saab")) # no token required
...
```

Some calls require a bearerToken. However, some calls are public and don't require a token.

[Where token?](#-blocket-api-token)


| Function  | Token required | Description  |
|---|---|---|
| [`api.saved_searches()`](#saved_searches) | 🔐 Yes | List your saved searches (bevakningar)  |
| [`api.get_listings()`](#get_listingssearch_id-limit) | 🔐 Yes | List items related to a saved search |
| [`api.custom_search()`](#custom_searchsearch_query-region-limit)  | 👏 No | Search for everything on Blocket and filter by region |
| [`api.motor_search()`](#motor_searchpage-make-fuel-chassi-price-modelyear-milage-gearbox)  | 👏 No | Advanced search for car-listings. |
| [`api.price_eval()`](#price_evalregistration_number)  | 👏 No | Vehicle purchase valuation and details. | 
| [`api.home_search()`](#home_searchcity-type-order_by-ordering-offset)  | 👏 No | Query home listings.

## 🤓 Detailed usage

### saved_searches()

Saved searches are your so called "Bevakningar" and can be found [here](https://www.blocket.se/sparade/bevakningar). Each saved search has and unique `id` which can be used as a parameter to `get_listings()`, see below.

```py
>>> api.saved_searches()
[
   {
      "id":"4150081",
      "new_count":0,
      "total_count":41,
      "push_enabled":false,
      "push_available":true,
      "query":"cg=1020&q=buggy&st=s",
      "name":"\"buggy\", Bilar säljes i hela Sverige"
   },
]
```

### get_listings(search_id, limit)
Returns all listings related to a saved search.

Parameters:
- `search_id` (`int`, optional) - Get listings for a specific saved search. If not provided, all saved searches will be combined.
- `limit` (`int`, optional) - Limit number of results returned, max is 99.

```py
>>> api.get_listings(4150081)
{
   "data":[
      {
         "ad":{
            "ad_id":"1401053984",
            "list_id":"1401053984",
            "zipcode":"81290",
            "ad_status":"active",
            "list_time":"2024-07-15T19:07:16+02:00",
            "subject":"Volkswagen 1500 lim 113 chassi",
            "body":"Säljer ett chassi/bottenplatta till en volkswagen 1500 lim 113 1967, blästrat och målat.\nFinns en beach buggy kaross att få med om man vill det. \nReg nmr ABC123",
            "price":{
               "value":10000,
               "suffix":"kr"
            },
            ...
         },
      },
   ],
   "total_count":41,
   "timestamp":"2024-07-16T08:08:43.810828006Z",
   "total_page_count":1
}
```

### custom_search(search_query, region, limit)
Make a custom search through out all of blocked. A region can be passed in as parameter for filtering.

Parameters:
- `search_query` (`str`, required) - A string to search for.
- `region` (`str`, optional) - Filter results on a region, default is all of Sweden.
- `limit` (`int`, optional) - Limit number of results returned, max is 99.

```py
>>> from blocket_api import Region
>>> api.custom_search("saab", Region.blekinge) # search for term "saab" in region of "Blekinge"
{
   "data":[
      {
         "ad_id":"1401038836",
         "ad_status":"active",
         "advertiser":{
            "account_id":"684279",
            "name":"Stefan Ingves",
            "type":"private"
         },
         ...
         "location":[
            {
               "id":"22",
               "name":"Blekinge",
               "query_key":"r"
            },
            {
               "id":"256",
               "name":"Ronneby",
               "query_key":"m"
            }
         ],
         ...
      }
    ]
}
```

### motor_search(page, make, fuel, chassi, price, modelYear, milage, gearbox)
To query listings related to a specific car, supply the following parameters:

- `page` (`int`, required) - Results are split in pages, set page number here.
- `make` (`List[MAKE_OPTIONS]`) - Filter a specific make, ex. `Audi`.
- `fuel` (`Optional[List[FUEL_OPTIONS]]`) - Filter a specific fuel, ex. `Diesel`.
- `chassi` (`Optional[List[CHASSI_OPTIONS]]`) - Filter a specific chassi, ex. `Cab`.
- `price` (`Optional[Tuple[int, int]]`) - Set price range, ex. `(50000, 100000)`.
- `modelYear` (`Optional[Tuple[int, int]]`) - Set model year range, ex. `(2000, 2020)`.
- `milage` (`Optional[Tuple[int, int]]`) - Set milage range, ex. `(1000, 2000)`.
- `gearbox` (`Optional[GEARBOX_OPTIONS]`) - Filter a specific gearbox, ex. `Automat`.
```py
>>> api.motor_search(
    make=["Audi", "Ford"],
    fuel=["Diesel"],
    chassi=["Cab"],
    price=(50000, 100000),
    page=1,
)
...
```

### price_eval(registration_number)
Query price evaluation for a specific vehicle by using cars registration number (ABC123). This returns company and private estimated prices, car information, and more. The api queries same endpoint as Blockets ["värdera bil"](https://www.blocket.se/tjanster/vardera-bil) service. 

- `registration_number` (`str`, required) - Registration number of the vehicle.
```py
>>> api.price_eval("ABC123)
{
   "registration_number": "ABC123",
   "private_valuation": 108155,
   "company_valuation": 108155,
   "car_info": {
      "make": "Volkswagen",
      "model": "Polo"
      ...
   }
   ...
}
```

### home_search(city, type, order_by, ordering, offset)
Query home listings from [bostad.blocket.se](https://bostad.blocket.se/).

- `city` (`str`, required) - City name, ex. Stockholm. 
- `type` (`HomeType`, optional) - Type of home, ex. `HomeType.apartment`.
- `order_by` (`OrderBy`, optional) - Sorting order, ex. `OrderBy.price`.
- `ordering` (`HOME_SEARCH_ORDERING`, optional) - Sorting order, ex. `"descending"`.
- `offset` (`int`, optional) - Offset for results, ex. `60`.

```py
>>> api.home_search(
    city="Stockholm",
    type=HomeType.apartment,
    order_by=OrderBy.price,
    ordering="descending",
)
...
```

## 🔐 Blocket API token

There are two ways to acquire your token:

- Log in to Blocket.se with your credentials using any web browser.
- Go to [this](https://www.blocket.se/api/adout-api-route/refresh-token-and-validate-session) URL and copy the value of `bearerToken`.

If there's a better way of doing this, feel free to help out in [#2](https://github.com/dunderrrrrr/blocket_api/issues/2).

Your token can also be found in the request headers in the "Bevakningar"-section on Blocket.

- **Login to [blocket.se](https**://blocket.se/)**: Sign in with your credentials.
- **Click "Bevakningar"**: Go to the "Bevakningar" section.
- **Inspect the page**: Right-click the page and select "Inspect".
- **Open the Network tab**: Switch to the Network tab in the Developer Tools.
- **Find request headers**: Locate a request where the domain is "api.blocket.se" and the file is "searches". *Pretty much every request to api.blocket.se contains this auth-header, so any request will do.*
- **Inspect request headers**: Look at the request headers to find your token under "Authorization".

![token](https://i.imgur.com/E5ofN0e.png)

My token has never expired or changed during this project. However, if your're met with a `401 Unauthorized` at some point, you may want to refresh your token by repeating the steps above.

## 📝 Notes

- Source repo: https://github.com/dunderrrrrr/blocket_api
- PyPI: https://pypi.org/project/blocket-api/
