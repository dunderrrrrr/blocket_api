# Examples

This is some very basic examples of how to use the API. For more details, see the [API reference](https://blocket-api.se/api-reference).

## Searching

### Search everything

Search for everything using keyword.

```python
import httpx

items = httpx.get(
    "https://blocket-api.se/v1/search",
    params={"query": "flipper zero", "sort_order": "PUBLISHED_DESC"},
).json()["docs"]

for item in items:
    data = httpx.get(
        "https://blocket-api.se/v1/ad/recommerce",
        params={"id": item["id"]},
    ).json()["loaderData"]["item-recommerce"]["itemData"]

    print(
        f"{data['title']}\n{data['description']}\n{data['price']}\n"
        f"{data['location']['postalName']}\n{item['canonical_url']}"
    )
    print("=" * 50)
```

Will return: 
```
Flipper zero
Fin flipper zero, knappt använd! Kan skickas.
2500
Stockholm
https://www.blocket.se/recommerce/forsale/item/19075245
==================================================
Flipper Zero oanvänd
Säljer Flipper Zero som bara legat och samlat damm efter att jag införskaffade den på en konferens i Sverige.
Förpackningen är endast öppnad för att fota innehållet.
2500
Linköping
https://www.blocket.se/recommerce/forsale/item/19053126
==================================================
Flipper zero
Flipper Zero säljes tillsammans med silikonskydd och extra tillbehör. Kort och flera taggar av olika slag följer med. Alla tillbehör är nya och oanvända. Flipper zero i nyskick. Se bilder för detaljer.
2450
Helsingborg
https://www.blocket.se/recommerce/forsale/item/18847358
==================================================
```

### Search for cars

```python
import httpx

response = httpx.get(
    "https://blocket-api.se/v1/search/car",
    params={
        "page": 1,
        "locations": "STOCKHOLM",
        "models": "AUDI",
        "price_from": 10000,
        "price_to": 50000,
        "year_from": 2010,
        "year_to": 2025,
    },
)

for item in response.json()["docs"]:
    print(f"({item["id"]})", item["price"]["amount"], "SEK -", item["heading"])
```

Will return: 

```
(18460933) 45000 SEK - Audi A4 Avant 2.0 TDI DPF Euro 5
(18566460) 45000 SEK - Audi A4 Avant 2.0 TFSI E85 Euro 5
(13436700) 10819 SEK - Audi A6 Avant e-tron Proline - Operationell leasing
(18712562) 50000 SEK - Audi A4 2.0 TDI Avant quattro (170hk)
```

### Get specific store ads

The id of the store can be found in the URL of the store page. For example, `https://www.blocket.se/mobility/search/car?orgId=XXXXXXXX` or `https://www.blocket.se/mobility/dealer/XXXXXX/store-name`.

```python
import httpx

response = httpx.get(
    "https://blocket-api.se/v1/search/car",
    params={
        "org_id": 1337,
        # see all available params in the swagger documentation
    },
)
```

## Get full ad details

Use the `/v1/ad/` endpoint to get full ad details.

```python
httpx.get(
    "https://blocket-api.se/v1/ad/car",
    params={"id": 1234},
)
```