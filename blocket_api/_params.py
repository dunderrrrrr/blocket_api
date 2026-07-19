from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from .constants import (
    SITE_URL,
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

_ParamValue = str | int | float | bool | None


def _build_params(
    defaults: dict[str, _ParamValue],
    extras: Sequence[tuple[str, _ParamValue]],
) -> list[tuple[str, _ParamValue]]:
    params: list[tuple[str, _ParamValue]] = [
        (k, v) for k, v in defaults.items() if v is not None
    ]
    params.extend(extras)
    return params


def build_search_params(
    query: str,
    *,
    page: int = 1,
    sort_order: SortOrder = SortOrder.RELEVANCE,
    locations: list[Location] = [],
    category: Category | None = None,
    sub_category: SubCategory | None = None,
) -> tuple[str, list[tuple[str, _ParamValue]]]:
    if category and sub_category:
        raise AssertionError("Cannot specify both category and sub_categories")

    url = f"{SITE_URL}/recommerce/forsale/search/api/search/SEARCH_ID_BAP_COMMON"

    defaults: dict[str, _ParamValue] = {
        "q": query,
        "page": page,
        "sort": sort_order.value,
        "category": category.value if category else None,
        "sub_category": sub_category.value if sub_category else None,
    }

    extras = [("location", loc.value) for loc in locations]

    return url, _build_params(defaults, extras)


def build_car_params(
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
) -> tuple[str, list[tuple[str, _ParamValue]]]:
    url = f"{SITE_URL}/mobility/search/api/search/SEARCH_ID_CAR_USED"

    defaults: dict[str, _ParamValue] = {
        "q": query,
        "page": page,
        "sort": sort_order.value,
        "price_from": price_from,
        "price_to": price_to,
        "year_from": year_from,
        "year_to": year_to,
        "milage_from": milage_from,
        "milage_to": milage_to,
        "engine_effect_from": horsepower_from,
        "engine_effect_to": horsepower_to,
        "orgId": org_id,
    }

    extras: list[tuple[str, _ParamValue]] = []
    extras.extend(("location", loc.value) for loc in locations)
    extras.extend(("make", model.value) for model in models)
    extras.extend(("exterior_colour", color.value) for color in colors)
    extras.extend(("transmission", t.value) for t in transmissions)
    extras.extend(("wheel_drive", w.value) for w in wheel_drive)

    return url, _build_params(defaults, extras)


def build_boat_params(
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
) -> tuple[str, list[tuple[str, _ParamValue]]]:
    url = f"{SITE_URL}/mobility/search/api/search/SEARCH_ID_BOAT_USED"

    defaults: dict[str, _ParamValue] = {
        "q": query,
        "page": page,
        "sort": sort_order.value,
        "price_from": price_from,
        "price_to": price_to,
        "length_feet_from": length_from,
        "length_feet_to": length_to,
        "orgId": org_id,
    }

    extras: list[tuple[str, _ParamValue]] = []
    extras.extend(("class", t.value) for t in types)
    extras.extend(("location", loc.value) for loc in locations)

    return url, _build_params(defaults, extras)


def build_mc_params(
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
) -> tuple[str, list[tuple[str, _ParamValue]]]:
    url = f"{SITE_URL}/mobility/search/api/search/SEARCH_ID_MC_USED"

    defaults: dict[str, _ParamValue] = {
        "q": query,
        "page": page,
        "sort": sort_order.value,
        "price_from": price_from,
        "price_to": price_to,
        "engine_volume_from": engine_volume_from,
        "engine_volume_to": engine_volume_to,
        "orgId": org_id,
    }

    extras: list[tuple[str, _ParamValue]] = []
    extras.extend(("make", m.value) for m in models)
    extras.extend(("location", loc.value) for loc in locations)
    extras.extend(("type", t.value) for t in types)

    return url, _build_params(defaults, extras)
