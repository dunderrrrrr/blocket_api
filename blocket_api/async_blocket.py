from __future__ import annotations

from typing import Any

import httpx

from ._params import (
    build_boat_params,
    build_car_params,
    build_mc_params,
    build_search_params,
)
from .ad_parser import BoatAd, CarAd, McAd, RecommerceAd
from .constants import (
    BOAT_SEARCH_URL,
    CAR_SEARCH_URL,
    HEADERS,
    MC_SEARCH_URL,
    SEARCH_URL,
)
from .constants import (
    BoatType,
    CarColor,
    CarModel,
    CarSortOrder,
    CarTransmission,
    CarWheelDrive,
    Category,
    Location,
    McModel,
    McSortOrder,
    McType,
    SortOrder,
    SubCategory,
)


class AsyncBlocketAPI:
    def __init__(self, client: httpx.AsyncClient | None = None) -> None:
        self._client = client or httpx.AsyncClient()
        self._owns_client = client is None

    async def __aenter__(self) -> AsyncBlocketAPI:
        return self

    async def __aexit__(self, *_: Any) -> None:
        await self.aclose()

    async def aclose(self) -> None:
        await self._client.aclose()

    async def search(
        self,
        query: str,
        *,
        page: int = 1,
        sort_order: SortOrder = SortOrder.RELEVANCE,
        locations: list[Location] = [],
        category: Category | None = None,
        sub_category: SubCategory | None = None,
    ) -> dict[str, Any]:
        params = build_search_params(
            query,
            page=page,
            sort_order=sort_order,
            locations=locations,
            category=category,
            sub_category=sub_category,
        )
        response = await self._client.get(SEARCH_URL, headers=HEADERS, params=params)
        response.raise_for_status()
        return response.json()

    async def search_car(
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
        horsepower_from: int | None = None,
        horsepower_to: int | None = None,
        wheel_drive: list[CarWheelDrive] = [],
        org_id: int | None = None,
    ) -> dict[str, Any]:
        params = build_car_params(
            query,
            page=page,
            sort_order=sort_order,
            locations=locations,
            models=models,
            price_from=price_from,
            price_to=price_to,
            year_from=year_from,
            year_to=year_to,
            milage_from=milage_from,
            milage_to=milage_to,
            colors=colors,
            transmissions=transmissions,
            horsepower_from=horsepower_from,
            horsepower_to=horsepower_to,
            wheel_drive=wheel_drive,
            org_id=org_id,
        )
        response = await self._client.get(
            CAR_SEARCH_URL, headers=HEADERS, params=params
        )
        response.raise_for_status()
        return response.json()

    async def search_boat(
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
        params = build_boat_params(
            query,
            page=page,
            sort_order=sort_order,
            types=types,
            locations=locations,
            price_from=price_from,
            price_to=price_to,
            length_from=length_from,
            length_to=length_to,
            org_id=org_id,
        )
        response = await self._client.get(
            BOAT_SEARCH_URL, headers=HEADERS, params=params
        )
        response.raise_for_status()
        return response.json()

    async def search_mc(
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
        params = build_mc_params(
            query,
            page=page,
            sort_order=sort_order,
            models=models,
            types=types,
            locations=locations,
            price_from=price_from,
            price_to=price_to,
            engine_volume_from=engine_volume_from,
            engine_volume_to=engine_volume_to,
            org_id=org_id,
        )
        response = await self._client.get(MC_SEARCH_URL, headers=HEADERS, params=params)
        response.raise_for_status()
        return response.json()

    async def get_ad(self, ad: RecommerceAd | CarAd | BoatAd | McAd) -> dict[str, Any]:
        response = await self._client.get(ad.url, headers=HEADERS)
        response.raise_for_status()
        return ad.parse(response)
