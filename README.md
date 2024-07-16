# BlocketAPI

BlocketAPI allows users to query saved searches, known as "Bevakningar", on [blocket.se](https://blocket.se/). This means you can either retrieve results from a specific saved search or list all listings/ads across all saved searches. The results from these queries are returned in a `json` format.

> Blocket is one of Sweden's largest online marketplaces. It was founded in 1996 and allows users to buy and sell a wide range of items, including cars, real estate, jobs, services, and second-hand goods. The platform is known for its extensive reach and user-friendly interface, making it a popular choice for Swedes looking to purchase or sell items quickly and efficiently.

## ✨ Features

- List saved searches, called "Bevakningar".
- Query all listings/ads filtered on a region.
- Query listings related to a saved search.

## 🧑‍💻️ Install

BlocketAPI is available on PyPI.

```sh
pip install blocket-api
```

## 💁‍♀️ Usage
```py
>>> from blocket_api import BlocketAPI
>>> api = BlocketAPI("YourBlocketTokenHere")
```

[Where token?](#-blocket-api-token)

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


## 🔓 Blocket API token

Your token is located in the request headers in the "Bevakningar"-section on Blocket.

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
