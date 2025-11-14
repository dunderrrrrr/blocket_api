<p align="center">
  <img src="https://blocket-api.se/blocket-api.png" />
</p>

# BlocketAPI

[![PyPI version](https://img.shields.io/pypi/v/blocket_api?style=for-the-badge)](https://pypi.org/project/blocket_api/) [![License](https://img.shields.io/badge/license-WTFPL-green?style=for-the-badge)](https://github.com/dunderrrrrr/blocket_api/blob/main/LICENSE) ![Python](https://img.shields.io/badge/Python-3.10-blue?style=for-the-badge) ![PyPI - Downloads](https://img.shields.io/pypi/dw/blocket_api?style=for-the-badge&color=%23dbce58) 

BlocketAPI allows users to query saved searches, known as "Bevakningar", on [blocket.se](https://blocket.se/). This means you can either retrieve results from a specific saved search or list all listings/ads across all saved searches. The results from these queries are returned in a `json` format or as cleaned pydantic objects.

> Blocket is one of Sweden's largest online marketplaces. It was founded in 1996 and allows users to buy and sell a wide range of items, including cars, real estate, jobs, services, and second-hand goods. The platform is known for its extensive reach and user-friendly interface, making it a popular choice for Swedes looking to purchase or sell items quickly and efficiently.

## ✨ Features

- List saved searches, called "Bevakningar".
- Get listings from all or a specific saved search.
- Search for anything on Blocket with filters for region and category.
- Get vehicle information, price evaluation and search for vehicles with multiple filters.
- Search for homes with filters for city, home type and more.
- Search for stores and get a specific store's listings.
- ...and more!

## 🧑‍💻️ Install

Install BlocketAPI via PyPI...

```sh
pip install blocket-api
```

or use [blocket-api.se](https://blocket-api.se) without installing anything!

## 💁‍♀️ Usage

```py
>>> from blocket_api import BlocketAPI
>>> api = BlocketAPI("YourBlocketTokenHere")
>>> print(api.saved_searches())
...
>>> print(BlocketAPI().custom_search("saab")) # no token required
...
```

Some calls require a `bearerToken`. However, some calls are public and don't require a token.

[Where token?](#-blocket-api-token)


| Function  | Token required | `as_objects` | Description  |
|---|---|---|---|
| [`api.saved_searches()`](#saved_searches) | 🔐 Yes | Yes | List your saved searches (bevakningar)  |
| [`api.get_listings()`](#get_listings) | 🔐 Yes | - | List items related to a saved search |
| [`api.custom_search()`](#custom_search)  | 👏 No | Yes | Search for everything on Blocket and filter by region |
| [`api.motor_search()`](#motor_search)  | 👏 No | Yes | Advanced search for car-listings. |
| [`api.price_eval()`](#price_eval)  | 👏 No | - | Vehicle purchase valuation and details. | 
| [`api.home_search()`](#home_search)  | 👏 No | Yes | Query home listings.
| [`api.store_search()`](#store_search)  | 👏 No | Yes | Search for a store.
| [`api.get_store_listings()`](#get_store_listings)  | 👏 No | Yes | Get listings from a specific store.
| [`api.get_ad_by_id()`](#get_ad_by_id)  | 👏 No | Yes | Get ad data from id.
| [`api.get_user_by_id()`](#get_user_by_id)  | 👏 No | Yes | Get user data from id.
| [`api.save_ad()`](#save_ad)  | 🔐 Yes | - | Save ad to "Saved ads".
| [`api.get_saved_ads()`](#get_saved_ads)  | 🔐 Yes | - | List all saved ads. 
| [`api.get_threads()`](#get_threads)  | 🔐 Yes | - | List all threads (messages).
| [`api.get_messages_from_thread()`](#get_messages_from_thread)  | 🔐 Yes | - | Get all messages from a thread. 
| [`api.unread_messages_count()`](#unread_messages_count)  | 🔐 Yes | Yes | Get the total count of unread messages.


## 🤓 Detailed usage

### saved_searches

Saved searches are your so called "Bevakningar" and can be found [here](https://www.blocket.se/sparade/bevakningar). Each saved search has and unique `id` which can be used as a parameter to `get_listings()`, see below.

Parameters:  
- `as_objects` (`bool`, optional) - Return results as pydantic models, default is `False`.

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

### get_listings
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

### custom_search
Make a custom search through out all of blocked. A region can be passed in as parameter for filtering.

Parameters:
- `search_query` (`str`, required) - A string to search for.
- `region` (`enum`, optional) - Filter results on a region, default is all of Sweden.
- `category` (`enum`, optional) - Filter for a specific category, ex. `Category.for_hemmet`.
- `limit` (`int`, optional) - Limit number of results returned, max is 99.
- `as_objects` (`bool`, optional) - Return results as pydantic models, default is `False`.

```py
>>> from blocket_api.blocket import Region, Category
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

### motor_search
To query listings related to a specific car, supply the following parameters:

- `page` (`int`, required) - Results are split in pages, set page number here.
- `make` (`List[MAKE_OPTIONS]`) - Filter a specific make, ex. `Audi`.
- `fuel` (`Optional[List[FUEL_OPTIONS]]`) - Filter a specific fuel, ex. `Diesel`.
- `chassi` (`Optional[List[CHASSI_OPTIONS]]`) - Filter a specific chassi, ex. `Cab`.
- `price` (`Optional[Tuple[int, int]]`) - Set price range, ex. `(50000, 100000)`.
- `modelYear` (`Optional[Tuple[int, int]]`) - Set model year range, ex. `(2000, 2020)`.
- `milage` (`Optional[Tuple[int, int]]`) - Set milage range, ex. `(1000, 2000)`.
- `gearbox` (`Optional[GEARBOX_OPTIONS]`) - Filter a specific gearbox, ex. `Automat`.
- `color` (`Optional[List[COLOR_OPTIONS]]`) - Filter a specific color.
- `as_objects` (`bool`, optional) - Return results as pydantic models, default is `False`.

```py
>>> api.motor_search(
    make=["Audi", "Ford"],
    fuel=["Diesel"],
    chassi=["Cab"],
    chassi=["Blå", "Röd"],
    price=(50000, 100000),
    page=1,
)
...
```

### price_eval
Query price evaluation for a specific vehicle by using cars registration number (ABC123). This returns company and private estimated prices, car information, and more. The api queries same endpoint as Blockets ["värdera bil"](https://www.blocket.se/tjanster/vardera-bil) service. 

- `registration_number` (`str`, required) - Registration number of the vehicle.
```py
>>> api.price_eval("ABC123")
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

### home_search
Query home listings from [bostad.blocket.se](https://bostad.blocket.se/).

- `city` (`str`, required) - City name, ex. Stockholm. 
- `type` (`HomeType`, optional) - Type of home, ex. `HomeType.apartment`.
- `order_by` (`OrderBy`, optional) - Sorting order, ex. `OrderBy.price`.
- `ordering` (`HOME_SEARCH_ORDERING`, optional) - Sorting order, ex. `"descending"`.
- `offset` (`int`, optional) - Offset for results, ex. `60`.
- `as_objects` (`bool`, optional) - Return results as pydantic models, default is False.

```py
>>> from blocket_api.qasa import HomeType, OrderBy
>>> api.home_search(
    city="Stockholm",
    type=HomeType.apartment,
    order_by=OrderBy.price,
    ordering="descending",
)
...
```

### store_search
Search for a store in Blocket stores from [blocket.se/butiker](https://www.blocket.se/butiker).

- `search_query` (`str`, required) - The name of the store. 
- `page` (`int`, optional) - The page number to return.
- `as_objects` (`bool`, optional) - Return results as pydantic models, default is `False`.


```py
>>> api.store_search("Jannes Car and Kebab")
{
  "data": [
    {
      "store_id": "1234",
      "store_name": "Jannes Car and Kebab",
      ...
    },
    ...
  ]
}
```

### get_store_listings
Get listings from a specific store.

- `store_id` (`int`, required) - The store id. Can be obtained by calling `store_search()`.
- `page` (`int`, optional) - The page number to return.
- `as_objects` (`bool`, optional) - Return results as pydantic models, default is `False`.


```py
>>> api.get_store_listings(1234)
{
  "data": [
    {
      "ad_id": "1234",
      "price": 316000,
      "body": "A very nice car.",
      "images": [],
      ...
    },
    ...
  ]
}
```

### get_ad_by_id
Get ad data from a specific ad id.

- `ad_id` (`int`, required) - The ad id. Can be found by calling any other method or from ad url.
- `as_objects` (`bool`, optional) - Return results as pydantic models, default is `False`.


```py
>>> api.get_ad_by_id(1234)
{
   "data": {
      "ad_id": "1234",
      "ad_status": "active",
      "advertiser": {...},
      "body": "A nice ad.",
      "category": [
            {"id": "4000", "name": "Personligt"},
            {"id": "4080", "name": "Kläder & skor"},
      ],
      ...
   }
}
```

### get_user_by_id
Get user data from a user id. User id can be found in ads, searches and in blocket url `https://www.blocket.se/profil/<user_id>`.

- `user_id` (`int`, required) - The blocket user id.
- `as_objects` (`bool`, optional) - Return results as pydantic models, default is `False`.


```py
>>> api.get_user_by_id(1234)
{
   'account': {
         'blocket_account_id': '1234', 
         'created_at': '2020-10-10T15:45:06.407660', 
         'is_verified': True, 
         'name': 'Janne',
         ...
   }, 
   'active_ads': {[
      ...
   ]}
}
```

### save_ad
This saves the ad to "Saved ads" which can be found here at `https://www.blocket.se/sparade/annonser`. When saving an ad, blocket always responds with 204, even if the ad is already saved or does not exist.

- `ad_id` (`int`, required) - The ad id. Can be found by calling any other method or from ad url.

```py
>>> api.save_ad(1234)
```

### get_saved_ads
Returns all of your saved ads from `https://www.blocket.se/sparade/annonser`.

```py
>>> api.get_saved_ads()
{
   'data': [{
      'ad_id': '1213682185'
      'list_id': '1213682185'
      'subject': 'Jeans från Gina tricot 158'
      'body': 'Moderna jeans från Gina Tricot!'
      ...
   }]
   ...
}

```

### get_threads
Returns all of your threads/conversations from Blocket. This api requires a token.

- `limit` (`int`, optional) - Number of threads to return, default is 15.

```py
>>> api = BlocketAPI("YourBlocketTokenHere")
>>> api.get_threads()
{
   "channels": [
      {     
         "channel_url": "sendbird_group_channel_123",
         "name": "from:user-id,ad:1214281684,to:c1-user-id",
         "data": {
            "ad": {
               "id": "1214281684",
               "advertiser_name": "Kalle",
               "subject": "Elsparkcykel",
               "status": "active",
               "url": "https://www.blocket.se/annons/1214281684",
               "price": "2 400 kr"
            },
         },
      },
      ...
   ],
}
```



### get_messages_from_thread
Returns all of your messages from an existing thread/conversation.

- `channel_id` (`str`, required) - The channel id to fetch messages from.

```py
>>> api = BlocketAPI("YourBlocketTokenHere")
>>> api.get_messages_from_thread("sendbird_group_channel_123")
{
   "messages": [
      {
         "type": "MESG",
         "message_id": 1354913370,
         "message": "Hey, is your thing still for sale?",
         ...
      },
   ],
}
```

### unread_messages_count
Returns the count of unread messages.

```py
>>> api = BlocketAPI("YourBlocketTokenHere")
>>> api.unread_messages_count()
{
   "unread_count": 5
}
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

- REST API: https://blocket-api.se
- Source repo: https://github.com/dunderrrrrr/blocket_api
- PyPI: https://pypi.org/project/blocket-api/
