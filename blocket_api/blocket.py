from __future__ import annotations
import httpx
from enum import Enum
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from httpx import Response


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


BASE_URL = "https://api.blocket.se"


class APIError(Exception): ...


class LimitError(Exception): ...


def _make_request(*, url, token: str, raise_for_status: bool = True) -> Response:
    try:
        response = httpx.get(
            url,
            headers={
                "Authorization": f"Bearer {token}",
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
            },
        )
        if raise_for_status:
            response.raise_for_status()
    except Exception as E:
        raise APIError(E)
    return response


@dataclass
class BlocketAPI:
    token: str

    def saved_searches(self) -> list[dict]:
        """
        Retrieves saved searches data, also known as "Bevakningar".
        """
        searches = (
            _make_request(url=f"{BASE_URL}/saved/v2/searches", token=self.token)
            .json()
            .get("data", [])
        )
        mobility_searches = (
            _make_request(
                url=f"{BASE_URL}/mobility-saved-searches/v1/searches", token=self.token
            )
            .json()
            .get("data", [])
        )

        return searches + mobility_searches

    def _for_search_id(self, search_id: int, limit: int) -> dict:
        searches = _make_request(
            url=f"{BASE_URL}/saved/v2/searches_content/{search_id}?lim={limit}",
            token=self.token,
            raise_for_status=False,
        )
        if searches.status_code == 404:
            mobility_searches = _make_request(
                url=f"{BASE_URL}/mobility-saved-searches/v1/searches/{search_id}/ads?lim={limit}",
                token=self.token,
                raise_for_status=True,
            )
            return mobility_searches.json()
        return searches.json()

    def get_listings(self, search_id: int | None = None, limit: int = 99) -> dict:
        """
        Retrieve listings/ads based on the provided search criteria.
        """
        if limit > 99:
            raise LimitError("Limit cannot be greater than 99.")

        if search_id:
            return self._for_search_id(search_id, limit)

        return _make_request(
            url=BASE_URL + f"/saved/v2/searches_content?lim={limit}",
            token=self.token,
        ).json()

    def custom_search(
        self, search_query: str, region: Region = Region.hela_sverige, limit: int = 99
    ) -> dict:
        """
        Do a custom search through out all of Blocket.
        Supply a region for filtering. Default is all of Sweden.
        """
        if limit > 99:
            raise LimitError("Limit cannot be greater than 99.")

        return _make_request(
            url=f"{BASE_URL}/search_bff/v2/content?lim={limit}&q={search_query}&r={region.value}&status=active",
            token=self.token,
        ).json()
