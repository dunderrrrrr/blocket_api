from dataclasses import dataclass
from enum import Enum
from typing import Literal

import httpx

from .constants import QASA_URL

HOME_SEARCH_ORDERING = Literal["descending", "ascending"]


class OrderBy(Enum):
    published_at = "published_or_bumped_at"
    price = "monthly_cost_cents"
    size = "square_meters"
    move_in_date = "start_date"
    move_out_date = "end_date"


class HomeType(Enum):
    apartment = ["apartment", "loft"]
    house = ["house", "terrace_house", "duplex"]
    cottage = ["cottage"]
    corridor = ["corridor", "room"]
    other = ["other"]


@dataclass
class Qasa:
    city: str
    home_type: HomeType
    order_by: OrderBy
    ordering: HOME_SEARCH_ORDERING
    offset: int

    def _construct_payload(self) -> dict:
        return {
            "operationName": "HomeSearch",
            "variables": {
                "limit": 60,  # no more than 60 items per page is allowed
                "offset": 0,
                "order": {
                    "direction": f"{self.ordering}",
                    "orderBy": f"{self.order_by.value}",
                },
                "params": {
                    "currency": "SEK",
                    "homeType": self.home_type.value,
                    "areaIdentifier": [f"se/{self.city}"],
                    "rentalType": ["long_term"],
                    "markets": ["sweden"],
                },
            },
            "query": """
                query HomeSearch(
                    $order: HomeIndexSearchOrderInput, 
                    $offset: Int, 
                    $limit: Int, 
                    $params: HomeSearchParamsInput
                ) {
                    homeIndexSearch(order: $order, params: $params) {
                        documents(offset: $offset, limit: $limit) {
                            hasNextPage
                            hasPreviousPage
                            nodes {
                                bedroomCount
                                blockListing
                                rentalLengthSeconds
                                householdSize
                                corporateHome
                                description
                                endDate
                                firstHand
                                furnished
                                homeType
                                id
                                instantSign
                                market
                                lastBumpedAt
                                monthlyCost
                                petsAllowed
                                platform
                                publishedAt
                                publishedOrBumpedAt
                                earlyAccessEndsAt
                                rent
                                currency
                                roomCount
                                seniorHome
                                shared
                                shortcutHome
                                smokingAllowed
                                sortingScore
                                squareMeters
                                startDate
                                studentHome
                                tenantBaseFee
                                title
                                wheelchairAccessible
                                location {
                                    id
                                    locality
                                    countryCode
                                    streetNumber
                                    point {
                                    lat
                                    lon
                                    __typename
                                    }
                                    route
                                    __typename
                                }
                                displayStreetNumber
                                uploads {
                                    id
                                    order
                                    type
                                    url
                                    __typename
                                }
                                __typename
                            }
                            pagesCount
                            totalCount
                            __typename
                        }
                    __typename
                    }
                }""",
        }

    def search(self) -> dict:
        query = self._construct_payload()

        response = httpx.post(QASA_URL, json=query)
        response.raise_for_status()
        return response.json()
