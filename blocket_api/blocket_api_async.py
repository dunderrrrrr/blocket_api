from __future__ import annotations

from collections.abc import Callable
from functools import wraps
import urllib
from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, Any, List, Literal, Optional, Tuple
from bs4 import BeautifulSoup
import json

import httpx

if TYPE_CHECKING:
    from httpx import Response

BASE_URL = "https://api.blocket.se"
SITE_URL = "https://www.blocket.se"
BYTBIL_URL = "https://api.bytbil.com"


class Region(Enum):
    hela_sverige = 0
    östergötland = 14
    blekinge = 22
    dalarna = 6
    gotland = 19
    gävleborg = 5
    göteborg = 15
    halland = 20
    jämtland = 3
    jönköping = 17
    kalmar = 18
    kronoberg = 21
    norrbotten = 1
    skaraborg = 13
    skåne = 23
    stockholm = 11
    södermanland = 12
    uppsala = 10
    värmland = 7
    västerbotten = 2
    västernorrland = 4
    västmanland = 9
    älvsborg = 16
    örebro = 8


MAKE_OPTIONS = Literal[
    "Audi",
    "BMW",
    "Chevrolet",
    "Citroën",
    "Ford",
    "Honda",
    "Hyundai",
    "Kia",
    "Mazda",
    "Mercedes-Benz",
    "Nissan",
    "Opel",
    "Peugeot",
    "Renault",
    "Saab",
    "Skoda",
    "Subaru",
    "Toyota",
    "Volkswagen",
    "Volvo",
]

FUEL_OPTIONS = Literal["Diesel", "Bensin", "El", "Miljöbränsle/Hybrid"]
CHASSI_OPTIONS = Literal[
    "Kombi", "SUV", "Sedan", "Halvkombi", "Coupé", "Cab", "Familjebuss", "Yrkesfordon"
]
GEARBOX_OPTIONS = Literal["Automat", "Manuell"]


class APIError(Exception): ...


class LimitError(Exception): ...


class TokenError(Exception): ...


def auth_token(method: Callable) -> Callable:
    @wraps(method)
    async def wrapper(self: Any, *args: Any, **kwargs: Any) -> Any:
        if not self.token:
            raise TokenError("Token is required, see documentation.")
        return await method(self, *args, **kwargs)

    return wrapper


def public_token(method: Callable) -> Callable:
    @wraps(method)
    async def wrapper(self: Any, *args: Any, **kwargs: Any) -> Any:
        if not self.token:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{SITE_URL}/api/adout-api-route/refresh-token-and-validate-session"
                )
                response.raise_for_status()
                self.token = response.json()["bearerToken"]
        return await method(self, *args, **kwargs)

    return wrapper


async def _make_request(
    *, url: str, token: str | None, raise_for_status: bool = True
) -> Response:
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0"
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers)
            if raise_for_status:
                response.raise_for_status()
        except Exception as E:
            raise APIError(E)
        return response


@dataclass
class BlocketAPIAsync:
    token: str | None = None

    @auth_token
    async def saved_searches(self) -> list[dict]:
        """
        Retrieves saved searches data, also known as "Bevakningar".
        """
        assert self.token

        searches_response = await _make_request(url=f"{BASE_URL}/saved/v2/searches", token=self.token)
        searches = searches_response.json().get("data", [])

        mobility_searches_response = await _make_request(
            url=f"{BASE_URL}/mobility-saved-searches/v1/searches", token=self.token
        )
        mobility_searches = mobility_searches_response.json().get("data", [])

        return searches + mobility_searches

    async def _for_search_id(self, search_id: int, limit: int) -> dict:
        assert self.token
        searches = await _make_request(
            url=f"{BASE_URL}/saved/v2/searches_content/{search_id}?lim={limit}",
            token=self.token,
            raise_for_status=False,
        )
        if searches.status_code == 404:
            mobility_searches = await _make_request(
                url=f"{BASE_URL}/mobility-saved-searches/v1/searches/{search_id}/ads?lim={limit}",
                token=self.token,
                raise_for_status=True,
            )
            return mobility_searches.json()
        return searches.json()

    @auth_token
    async def get_listings(self, search_id: int | None = None, limit: int = 99) -> dict:
        """
        Retrieve listings/ads based on the provided search criteria.
        """
        assert self.token

        if limit > 99:
            raise LimitError("Limit cannot be greater than 99.")

        if search_id:
            return await self._for_search_id(search_id, limit)

        response = await _make_request(
            url=BASE_URL + f"/saved/v2/searches_content?lim={limit}",
            token=self.token,
        )
        return response.json()

    @public_token
    async def custom_search(
        self, search_query: str, region: Region = Region.hela_sverige, limit: int = 99
    ) -> dict:
        """
        Do a custom search through out all of Blocket.
        Supply a region for filtering. Default is all of Sweden.
        """
        assert self.token

        if limit > 99:
            raise LimitError("Limit cannot be greater than 99.")

        response = await _make_request(
            url=f"{BASE_URL}/search_bff/v2/content?lim={limit}&q={search_query}&r={region.value}&status=active",
            token=self.token,
        )
        return response.json()

    @public_token
    async def motor_search(
        self,
        page: int,
        make: List[MAKE_OPTIONS],
        fuel: Optional[List[FUEL_OPTIONS]] = None,
        chassi: Optional[List[CHASSI_OPTIONS]] = None,
        price: Optional[Tuple[int, int]] = None,
        modelYear: Optional[Tuple[int, int]] = None,
        milage: Optional[Tuple[int, int]] = None,
        gearbox: Optional[GEARBOX_OPTIONS] = None,
    ) -> dict:
        """
        Search specifically in the car section of Blocket
        with set optional parameters for filtering.
        """
        assert self.token

        range_params = ["price", "modelYear", "milage"]
        set_params = {
            key: value
            for key, value in locals().items()
            if key not in ["self", "page", "range_params"] and value is not None
        }

        filters = []
        for param, value in set_params.items():
            filter = {"key": param, "values": value}
            if param in range_params:
                range_start, range_end = filter.pop("values")
                filter["range"] = {
                    "start": str(range_start),
                    "end": str(range_end),
                }
            filter_str = urllib.parse.quote(str(filter).replace("'", '"'))
            filters.append(filter_str)

        motor_base_url = f"{BASE_URL}/motor-search-service/v4/search/car"

        filters_str = "&".join([f"filter={f}" for f in filters])
        url = f"{motor_base_url}?{filters_str}&page={page}"

        response = await _make_request(url=f"{url}", token=self.token)
        return response.json()

    @public_token
    async def car_listing_info(
        self, listing_url: int| None = None
    ) -> dict:
        """
        Get detailed information about a specific car listing by its ID.
        """
        response = await _make_request(url=listing_url, token=self.token)
        # get the __next_js__ element
        if response.status_code == 404:
            raise APIError("Listing not found or has been removed.")
        html = await response.text()
        soup = BeautifulSoup(html, 'html.parser')
        script_tag = soup.find('script', id='__NEXT_DATA__')
        # parse the JSON data from the script tag

        data = json.loads(script_tag.string)
        d = data.get('props', {}).get('pageProps', {}).get('initialReduxState', {}).get('classified', {}).get('requestedAd', {}).get('ad', {})
        return d



    @public_token
    async def price_eval(
        self,
        registration_number: str,
    ) -> dict:
        """
        Price evaluation for a specific vehicle by using cars
        registration number (ABC123).

        This is using same api endpoint as https://www.blocket.se/tjanster/vardera-bil.
        """
        url = f"{BYTBIL_URL}/blocket-basedata-api/v3/vehicle-data/{registration_number}"
        response = await _make_request(url=f"{url}", token=None)
        return response.json()
