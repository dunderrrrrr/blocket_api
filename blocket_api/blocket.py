from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import httpx
from httpx import Response

from .ad_parser import BoatAd, CarAd, McAd, RecommerceAd
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
    McModel,
    McSortOrder,
    McType,
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
        page: int = 1,
        sort_order: SortOrder = SortOrder.RELEVANCE,
        locations: list[Location] = [],
        category: Category | None = None,
        sub_category: SubCategory | None = None,
    ) -> dict[str, Any]:
        if category and sub_category:
            raise AssertionError("Cannot specify both category and sub_categories")

        url = f"{SITE_URL}/recommerce/forsale/search/api/search/SEARCH_ID_BAP_COMMON"

        param_dict: dict[str, str | int | None] = {
            "q": query,
            "page": page,
            "sort": sort_order.value,
            "category": category.value if category else None,
            "sub_category": sub_category.value if sub_category else None,
        }

        params = [QueryParam(k, v) for k, v in param_dict.items() if v is not None]

        params.extend(QueryParam("location", loc.value) for loc in locations)

        return _request(url=url, params=params).json()

    def search_car(
        self,
        query: str | None = None,
        *,
        page: int = 1,
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
        org_id: int | None = None,
    ) -> dict[str, Any]:
        url = f"{SITE_URL}/mobility/search/api/search/SEARCH_ID_CAR_USED"

        param_dict: dict[str, str | int | None] = {
            "q": query,
            "page": page,
            "sort": sort_order.value,
            "price_from": price_from,
            "price_to": price_to,
            "year_from": year_from,
            "year_to": year_to,
            "milage_from": milage_from,
            "milage_to": milage_to,
            "org_id": org_id,
        }

        params = [QueryParam(k, v) for k, v in param_dict.items() if v is not None]

        # Multi-value params
        params.extend(QueryParam("location", loc.value) for loc in locations)
        params.extend(QueryParam("make", model.value) for model in models)
        params.extend(QueryParam("exterior_colour", color.value) for color in colors)
        params.extend(QueryParam("transmission", t.value) for t in transmissions)

        return _request(url=url, params=params).json()

    def search_boat(
        self,
        query: str | None = None,
        *,
        page: int = 1,
        sort_order: CarSortOrder = CarSortOrder.RELEVANCE,
        types: list[BoatType] = [],
        locations: list[Location] = [],
        price_from: int | None = None,
        price_to: int | None = None,
        length_from: int | None = None,
        length_to: int | None = None,
        org_id: int | None = None,
    ) -> Any:
        url = f"{SITE_URL}/mobility/search/api/search/SEARCH_ID_BOAT_USED"

        param_dict: dict[str, str | int | None] = {
            "q": query,
            "page": page,
            "sort": sort_order.value,
            "price_from": price_from,
            "price_to": price_to,
            "length_feet_from": length_from,
            "length_feet_to": length_to,
            "org_id": org_id,
        }

        params = [QueryParam(k, v) for k, v in param_dict.items() if v is not None]

        params.extend(QueryParam("class", t.value) for t in types)
        params.extend(QueryParam("location", loc.value) for loc in locations)

        return _request(url=url, params=params).json()

    def search_mc(
        self,
        query: str | None = None,
        *,
        page: int = 1,
        sort_order: McSortOrder = McSortOrder.RELEVANCE,
        models: list[McModel] = [],
        types: list[McType] = [],
        locations: list[Location] = [],
        price_from: int | None = None,
        price_to: int | None = None,
        engine_volume_from: int | None = None,
        engine_volume_to: int | None = None,
        org_id: int | None = None,
    ) -> dict[str, Any]:
        url = f"{SITE_URL}/mobility/search/api/search/SEARCH_ID_MC_USED"

        param_dict: dict[str, str | int | None] = {
            "q": query,
            "page": page,
            "sort": sort_order.value,
            "price_from": price_from,
            "price_to": price_to,
            "engine_volume_from": engine_volume_from,
            "engine_volume_to": engine_volume_to,
            "org_id": org_id,
        }

        params = [QueryParam(k, v) for k, v in param_dict.items() if v is not None]

        params.extend(QueryParam("make", m.value) for m in models)
        params.extend(QueryParam("location", loc.value) for loc in locations)
        params.extend(QueryParam("type", t.value) for t in types)

        return _request(url=url, params=params).json()

    def get_ad(self, ad: RecommerceAd | CarAd | BoatAd | McAd) -> dict[str, Any]:
        response = _request(url=ad.url, params=[])
        return ad.parse(response)
