from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import httpx

from .constants import HEADERS, SITE_URL, Category, Location, SortOrder, SubCategory


@dataclass(frozen=True)
class QueryParam:
    name: str
    value: str


def _request(
    *,
    url: str,
    params: list[QueryParam],
) -> Any:
    response = httpx.get(
        url,
        headers=HEADERS,
        params=[(param.name, param.value) for param in params],
    )
    response.raise_for_status()
    return response.json()


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

        return _request(url=url, params=params)
