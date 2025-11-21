from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import httpx
from httpx import Response

from .ad_parser import BoatAd, CarAd, RecommerceAd
from .constants import (
    HEADERS,
    SITE_URL,
    BoatType,
    CarColor,
    CarModel,
    CarSortOrder,
    CarTransmission,
    Category,
    Location,
    SortOrder,
    SubCategory,
)


@dataclass(frozen=True)
class QueryParam:
    name: str
    value: str | int


def _request(*, url: str, params: list[QueryParam]) -> Response:
    response = httpx.get(
        url,
        headers=HEADERS,
        params=[(param.name, param.value) for param in params],
    )
    response.raise_for_status()
    return response


@dataclass(frozen=True)
class BlocketAPI:
    def search(
        self,
        query: str,
        *,
        sort_order: SortOrder = SortOrder.RELEVANCE,
        locations: list[Location] = [],
        category: Category | None = None,
        sub_category: SubCategory | None = None,
    ) -> Any:
        if category and sub_category:
            raise AssertionError("Cannot specify both category and sub_categories")

        url = f"{SITE_URL}/recommerce-search-page/api/search/SEARCH_ID_BAP_COMMON"
        params = [
            QueryParam("q", query),
            QueryParam("sort", sort_order.value),
            *[QueryParam("location", location.value) for location in locations],
            *([QueryParam("category", category.value)] if category else []),
            *([QueryParam("sub_category", sub_category.value)] if sub_category else []),
        ]

        return _request(url=url, params=params).json()

    def search_car(
        self,
        query: str | None = None,
        *,
        sort_order: CarSortOrder = CarSortOrder.RELEVANCE,
        locations: list[Location] = [],
        models: list[CarModel] = [],
        price_from: int | None = None,
        price_to: int | None = None,
        year_from: int | None = None,
        year_to: int | None = None,
        milage_from: int | None = None,
        milage_to: int | None = None,
        colors: list[CarColor] = [],
        transmissions: list[CarTransmission] = [],
    ) -> Any:
        url = f"{SITE_URL}/mobility/search/api/search/SEARCH_ID_CAR_USED"
        params = [
            *([QueryParam("q", query)] if query else []),
            QueryParam("sort", sort_order.value),
            *[QueryParam("location", location.value) for location in locations],
            *[QueryParam("make", model.value) for model in models],
            *([QueryParam("price_from", price_from)] if price_from else []),
            *([QueryParam("price_to", price_to)] if price_to else []),
            *([QueryParam("year_from", year_from)] if year_from else []),
            *([QueryParam("year_to", year_to)] if year_to else []),
            *([QueryParam("milage_from", milage_from)] if milage_from else []),
            *([QueryParam("milage_to", milage_to)] if milage_to else []),
            *[QueryParam("exterior_colour", color.value) for color in colors],
            *[QueryParam("transmission", t.value) for t in transmissions],
        ]

        return _request(url=url, params=params).json()

    def search_boat(
        self,
        query: str | None = None,
        *,
        sort_order: CarSortOrder = CarSortOrder.RELEVANCE,
        types: list[BoatType] = [],
        locations: list[Location] = [],
        price_from: int | None = None,
        price_to: int | None = None,
        length_from: int | None = None,
        length_to: int | None = None,
    ) -> Any:
        url = f"{SITE_URL}/mobility/search/api/search/SEARCH_ID_BOAT_USED"
        params = [
            *([QueryParam("q", query)] if query else []),
            QueryParam("sort", sort_order.value),
            *[QueryParam("class", t.value) for t in types],
            *[QueryParam("location", location.value) for location in locations],
            *([QueryParam("price_from", price_from)] if price_from else []),
            *([QueryParam("price_to", price_to)] if price_to else []),
            *([QueryParam("length_feet_from", length_from)] if length_from else []),
            *([QueryParam("length_feet_to", length_to)] if length_to else []),
        ]
        return _request(url=url, params=params).json()

    def get_ad(self, ad: RecommerceAd | CarAd | BoatAd) -> dict:
        response = _request(url=ad.url, params=[])
        return ad.parse(response)
