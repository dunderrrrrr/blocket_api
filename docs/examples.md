# Examples

## Making a custom search

```bash
curl -X 'GET' \
  'https://blocket-api.se/v1/custom-search?query=pool&region=dalarna&category=for_hemmet&limit=99' \
  -H 'accept: application/json'
```

```python
import httpx

response = httpx.get(
    "https://blocket-api.se/v1/custom-search",
    params={
        "query": "pool",
        "region": "dalarna",
        "category": "for_hemmet",
        "limit": 99,
    },
    headers={"accept": "application/json"}
)
print(response.json())

```

## Searching for a specific car

```bash
curl -X 'GET' \
  'https://blocket-api.se/v1/motor-search?page=0&make=Audi&make=BMW&fuel=Diesel&fuel=Bensin&chassi=Kombi&chassi=SUV&chassi=Sedan&gearbox=Automat&price_lower=10000&price_upper=50000&model_year_lower=2010&model_year_upper=2025&milage_lower=10&milage_upper=70000' \
  -H 'accept: application/json'
```

```python
import httpx

response = httpx.get(
    "https://blocket-api.se/v1/motor-search",
    params={
        "page": 0,
        "make": ["Audi", "BMW"],
        "fuel": ["Diesel", "Bensin"],
        "chassi": ["Kombi", "SUV", "Sedan"],
        "gearbox": "Automat",
        "price_lower": 10000,
        "price_upper": 50000,
        "model_year_lower": 2010,
        "model_year_upper": 2025,
        "milage_lower": 10,
        "milage_upper": 70000
    },
    headers={"accept": "application/json"}
)
print(response.json())

```

## Using your saved searches
```python
import httpx

BASE_URL = "https://blocket-api.se/v1"
TOKEN = "replace_with_your_token"

def get_saved_searches(token: str):
    response = httpx.get(f"{BASE_URL}/saved-searches", params={"token": token})
    response.raise_for_status()
    return response.json()

def get_listings_for_search(token: str, search_id: str):
    response = httpx.get(
        f"{BASE_URL}/get-listings", params={"token": token, "search_id": search_id}
    )
    response.raise_for_status()
    return response.json()["data"]

def print_listing(ad):
    ad_data = ad["ad"]
    print(
        f"Subject: {ad_data['subject']}\n"
        f"Is New: {ad['is_new']}\n"
        f"Price: {ad_data['price']}\n"
        "------------------------"
    )

if __name__ == "__main__":
    saved_searches = get_saved_searches(TOKEN)

    for custom_search in saved_searches:
        listings = get_listings_for_search(TOKEN, custom_search["id"])
        for ad in listings:
            print_listing(ad)

```

### Creating a saved search

Blocket.se has a bunch of filters. All filters are not available as query parameters yet. But do not fear! All options/filters blocket has can be used by this api and the python library. 

Over at Blocket, you can make a custom search (or a so called saved search). This custom search can then be used as a "pre-made filter", which can then be used by the api. Blocket calls it [bevakningar](https://blocket.zendesk.com/hc/sv/articles/22875498207506-Bevakningar). 

Let's say we want to filter to red Volkswagens. Go ahead and make the filtering at blocket.se. Once done, click "Skapa bevakning". When your search is saved you can use `/v1/saved-searches` to list all your saved searches. Grab the `id` and use that together with `/v1/get-listings`. See example above.

This endpoint will require a `token` parameter, since it's an endpoint that's only available to logged in users.

## Get a specific ad by id

```bash
curl -X 'GET' \
  'https://blocket-api.se/v1/get-ad-by-id?ad_id=123456789' \
  -H 'accept: application/json'
```

```python
import httpx

response = httpx.get(
    "https://blocket-api.se/v1/get-ad-by-id",
    params={"ad_id": 123456789},
    headers={"accept": "application/json"}
)
print(response.json())
```

## Get a user from id

The user id can be found in the url or in ads data using any other endpoint. 

```bash
curl -X 'GET' \
  'https://blocket-api.se/v1/get-user-by-id?user_id=123456789' \
  -H 'accept: application/json'
```

```python
import httpx

response = httpx.get(
    "https://blocket-api.se/v1/get-user-by-id",
    params={"ad_id": 123456789},
    headers={"accept": "application/json"}
)
print(response.json())
```

## Using endpoints with token

```sh
# Token as header (preferred)
curl -X 'GET' \
  'https://blocket-api.se/v1/save-ad?ad_id=1234' \
  -H 'accept: application/json' \
  -H 'X-Token: abc123'

# Token as query parameter
curl -X 'GET' \
  'https://blocket-api.se/v1/save-ad?ad_id=1234&token=abc123' \
  -H 'accept: application/json'
```

```python
# Token as header (preferred)
httpx.get(
    "https://blocket-api.se/v1/save-ad",
    params={"ad_id": 1234},
    headers={
        "accept": "application/json",
        "X-Token": "abc123",
    }
)

# Token as query parameter
httpx.get(
    "https://blocket-api.se/v1/save-ad",
    params={
        "ad_id": 1234,
        "token": "abc123",
    },
    headers={"accept": "application/json"}
)
```