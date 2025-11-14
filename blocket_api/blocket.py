from __future__ import annotations

import urllib
from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, List, Literal, Optional, Tuple, Union, overload

import httpx

from blocket_api.models import (
    AdByIdResults,
    BlocketUser,
    CustomSearchResults,
    HomeSearchResults,
    MotorSearchResults,
    SavedSearchResponse,
    StoreListings,
    StoreSearchResults,
    UnreadMessagesCount,
)
from blocket_api.qasa import HOME_SEARCH_ORDERING, HomeType, OrderBy, Qasa

from .constants import BASE_URL, BYTBIL_URL
from .decorators import auth_token, public_token
from .sendbird import Sendbird

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


class Category(Enum):
    fordon = 1000
    bilar = 1020
    bildelar_biltillbehor = 1040
    batar = 1060
    batdelar_tillbehor = 1080
    husvagnar_husbilar = 1100
    mopeder_a_traktor = 1120
    motorcyklar = 1140
    mc_delar_tillbehor = 1160
    lastbil_truck_entreprenad = 1220
    skogs_lantbruksmaskiner = 1240
    snoskotrar = 1180
    snoskoterdelar_tillbehor = 1200
    for_hemmet = 2000
    bygg_tradgard = 2020
    mobler_heminredning = 2040
    husgerad_vitvaror = 2060
    verktyg = 2026
    bostad = 3000
    lagenheter = 3020
    villor = 3100
    radhus = 3120
    tomter = 3060
    gardar = 3070
    fritidsboende = 3040
    utland = 3080
    personligt = 4000
    klader_skor = 4080
    accessoarer_klockor = 4060
    barnklader_skor = 4020
    barnartiklar_leksaker = 4040
    elektronik = 5000
    datorer_tv_spel = 5020
    ljud_bild = 5040
    telefoner_tillbehor = 5060
    fritid_hobby = 6000
    biljetter_resor = 6020
    bocker_studentlitteratur = 6040
    cyklar = 6060
    djur = 6080
    hobby_samlarprylar = 6100
    hastar_ridsport = 6120
    jakt_fiske = 6140


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
COLOR_OPTIONS = Literal["Blå", "Brun", "Grå", "Grön", "Gul", "Röd", "Svart", "Vit"]


class APIError(Exception): ...


class LimitError(Exception): ...


def _make_request(
    *,
    method: Callable[..., Response] = httpx.get,
    url: str,
    token: str | None,
    raise_for_status: bool = True,
) -> Response:
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0"
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    try:
        response = method(url, headers=headers)
        if raise_for_status:
            response.raise_for_status()
    except Exception as e:
        raise APIError(e)
    return response


@dataclass
class BlocketAPI:
    token: str | None = None

    @overload
    def saved_searches(
        self,
        limit: int = 99,
        *,
        as_objects: Literal[True],
    ) -> SavedSearchResponse: ...

    @overload
    def saved_searches(
        self,
        limit: int = 99,
        *,
        as_objects: Literal[False] = False,
    ) -> list[dict]: ...

    @auth_token
    def saved_searches(
        self,
        *,
        as_objects: bool = False,
    ) -> list[dict] | SavedSearchResponse:
        """
        Retrieves saved searches data, also known as "Bevakningar".
        """
        assert self.token

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

        result = searches + mobility_searches
        return SavedSearchResponse(searches=result) if as_objects else result

    def _for_search_id(self, search_id: int, limit: int) -> dict:
        assert self.token
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

    @auth_token
    def get_listings(self, search_id: int | None = None, limit: int = 99) -> dict:
        """
        Retrieve listings/ads based on the provided search criteria.
        """
        assert self.token

        if limit > 99:
            raise LimitError("Limit cannot be greater than 99.")

        if search_id:
            return self._for_search_id(search_id, limit)

        return _make_request(
            url=BASE_URL + f"/saved/v2/searches_content?lim={limit}",
            token=self.token,
        ).json()

    @overload
    def custom_search(
        self,
        search_query: str,
        region: Region = Region.hela_sverige,
        category: Category | None = None,
        limit: int = 99,
        *,
        as_objects: Literal[True],
    ) -> CustomSearchResults: ...

    @overload
    def custom_search(
        self,
        search_query: str,
        region: Region = Region.hela_sverige,
        category: Category | None = None,
        limit: int = 99,
        *,
        as_objects: Literal[False] = False,
    ) -> dict: ...

    @overload
    def custom_search(
        self,
        search_query: str,
        region: Region = Region.hela_sverige,
        category: Category | None = None,
        limit: int = 99,
        *,
        as_objects: bool = False,
    ) -> Union[dict, CustomSearchResults]: ...

    @public_token
    def custom_search(
        self,
        search_query: str,
        region: Region = Region.hela_sverige,
        category: Category | None = None,
        limit: int = 99,
        *,
        as_objects: bool = False,
    ) -> dict | CustomSearchResults:
        """
        Do a custom search throughout all of Blocket.
        """
        assert self.token

        if limit > 99:
            raise LimitError("Limit cannot be greater than 99.")

        url = f"{BASE_URL}/search_bff/v2/content?lim={limit}&q={search_query}&r={region.value}&status=active"

        if category:
            url += f"&cg={category.value}"

        response = _make_request(url=url, token=self.token).json()
        return CustomSearchResults.model_validate(response) if as_objects else response

    @overload
    def motor_search(
        self,
        page: int,
        make: List[MAKE_OPTIONS],
        fuel: Optional[List[FUEL_OPTIONS]] = None,
        chassi: Optional[List[CHASSI_OPTIONS]] = None,
        price: Optional[Tuple[int, int]] = None,
        modelYear: Optional[Tuple[int, int]] = None,
        milage: Optional[Tuple[int, int]] = None,
        gearbox: Optional[GEARBOX_OPTIONS] = None,
        *,
        as_objects: Literal[True],
    ) -> MotorSearchResults: ...

    @overload
    def motor_search(
        self,
        page: int,
        make: List[MAKE_OPTIONS],
        fuel: Optional[List[FUEL_OPTIONS]] = None,
        chassi: Optional[List[CHASSI_OPTIONS]] = None,
        price: Optional[Tuple[int, int]] = None,
        modelYear: Optional[Tuple[int, int]] = None,
        milage: Optional[Tuple[int, int]] = None,
        gearbox: Optional[GEARBOX_OPTIONS] = None,
        color: Optional[List[COLOR_OPTIONS]] = None,
        *,
        as_objects: Literal[False] = False,
    ) -> dict: ...

    @overload
    def motor_search(
        self,
        page: int,
        make: List[MAKE_OPTIONS],
        fuel: Optional[List[FUEL_OPTIONS]] = None,
        chassi: Optional[List[CHASSI_OPTIONS]] = None,
        price: Optional[Tuple[int, int]] = None,
        modelYear: Optional[Tuple[int, int]] = None,
        milage: Optional[Tuple[int, int]] = None,
        gearbox: Optional[GEARBOX_OPTIONS] = None,
        color: Optional[List[COLOR_OPTIONS]] = None,
        *,
        as_objects: bool = False,
    ) -> Union[dict, MotorSearchResults]: ...

    @public_token
    def motor_search(
        self,
        page: int,
        make: List[MAKE_OPTIONS],
        fuel: Optional[List[FUEL_OPTIONS]] = None,
        chassi: Optional[List[CHASSI_OPTIONS]] = None,
        price: Optional[Tuple[int, int]] = None,
        modelYear: Optional[Tuple[int, int]] = None,
        milage: Optional[Tuple[int, int]] = None,
        gearbox: Optional[GEARBOX_OPTIONS] = None,
        color: Optional[List[COLOR_OPTIONS]] = None,
        *,
        as_objects: bool = False,
    ) -> dict | MotorSearchResults:
        """
        Search specifically in the car section of Blocket
        with set optional parameters for filtering.
        """
        assert self.token

        range_params = ["price", "modelYear", "milage"]
        set_params = {
            key: value
            for key, value in locals().items()
            if key not in ["self", "page", "range_params", "as_objects"]
            and value is not None
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

        response = _make_request(url=f"{url}", token=self.token).json()
        return MotorSearchResults.model_validate(response) if as_objects else response

    @public_token
    def price_eval(
        self,
        registration_number: str,
    ) -> dict:
        """
        Price evaluation for a specific vehicle by using cars
        registration number (ABC123).

        This is using same api endpoint as https://www.blocket.se/tjanster/vardera-bil.
        """
        url = f"{BYTBIL_URL}/blocket-basedata-api/v3/vehicle-data/{registration_number}"
        return _make_request(url=f"{url}", token=None).json()

    @overload
    def home_search(
        self,
        city: str,
        type: HomeType,
        order_by: OrderBy = OrderBy.published_at,
        ordering: HOME_SEARCH_ORDERING = "descending",
        offset: int = 0,
        *,
        as_objects: Literal[True],
    ) -> HomeSearchResults: ...

    @overload
    def home_search(
        self,
        city: str,
        type: HomeType,
        order_by: OrderBy = OrderBy.published_at,
        ordering: HOME_SEARCH_ORDERING = "descending",
        offset: int = 0,
        *,
        as_objects: Literal[False] = False,
    ) -> dict: ...

    def home_search(
        self,
        city: str,
        type: HomeType,
        order_by: OrderBy = OrderBy.published_at,
        ordering: HOME_SEARCH_ORDERING = "descending",
        offset: int = 0,
        *,
        as_objects: bool = False,
    ) -> dict | HomeSearchResults:
        """
        This returns all available home listings available at
        https://bostad.blocket.se/. Specify offset to get next page. Each page contains
        60 items, which is max items returned per api query.
        """
        response = Qasa(
            city=city,
            home_type=type,
            order_by=order_by,
            ordering=ordering,
            offset=offset,
        ).search()
        return HomeSearchResults.model_validate(response) if as_objects else response

    @overload
    def search_store(
        self, search_query: str, page: int = 0, *, as_objects: Literal[True]
    ) -> StoreSearchResults: ...

    @overload
    def search_store(
        self, search_query: str, page: int = 0, *, as_objects: Literal[False] = False
    ) -> dict: ...

    @overload
    def search_store(
        self,
        page: int,
        make: List[MAKE_OPTIONS],
        fuel: Optional[List[FUEL_OPTIONS]] = None,
        chassi: Optional[List[CHASSI_OPTIONS]] = None,
        price: Optional[Tuple[int, int]] = None,
        modelYear: Optional[Tuple[int, int]] = None,
        milage: Optional[Tuple[int, int]] = None,
        gearbox: Optional[GEARBOX_OPTIONS] = None,
        *,
        as_objects: bool = False,
    ) -> Union[dict, StoreSearchResults]: ...

    @public_token
    def search_store(
        self,
        search_query: str,
        page: int = 0,
        *,
        as_objects: bool = False,
    ) -> dict | StoreSearchResults:
        """
        Searching through Blocket stores from https://www.blocket.se/butiker.
        The store_id is used for get_store_listings().
        """
        url = f"{BASE_URL}/search_bff/v1/stores?q={search_query}&page={page}"
        response = _make_request(url=f"{url}", token=self.token).json()
        return StoreSearchResults.model_validate(response) if as_objects else response

    @overload
    def get_store_listings(
        self, store_id: int, page: int = 0, *, as_objects: Literal[True]
    ) -> StoreListings: ...

    @overload
    def get_store_listings(
        self, store_id: int, page: int = 0, *, as_objects: Literal[False] = False
    ) -> dict: ...

    @public_token
    def get_store_listings(
        self,
        store_id: int,
        page: int = 0,
        *,
        as_objects: bool = False,
    ) -> dict | StoreListings:
        """
        Return all listings from a specific store from https://www.blocket.se/butik/<store>.
        The store_id can be found by searching for the store with search_store().
        """
        url = (
            f"{BASE_URL}/search_bff/v2/content?lim=60&page={page}&sort=rel&store_id={store_id}"
            "&status=active&gl=3&include=extend_with_shipping"
        )
        response = _make_request(url=f"{url}", token=self.token).json()
        return StoreListings.model_validate(response) if as_objects else response

    @overload
    def get_ad_by_id(
        self, ad_id: int, *, as_objects: Literal[True]
    ) -> AdByIdResults: ...

    @overload
    def get_ad_by_id(
        self, ad_id: int, *, as_objects: Literal[False] = False
    ) -> dict: ...

    @public_token
    def get_ad_by_id(
        self, ad_id: int, *, as_objects: bool = False
    ) -> dict | AdByIdResults:
        """
        Return an ad with it's content. The ad_id can be found by searching or
        from the blocket ad url.
        """
        url = f"{BASE_URL}/search_bff/v2/content/{ad_id}"
        response = _make_request(url=f"{url}", token=self.token).json()
        return AdByIdResults.model_validate(response) if as_objects else response

    @overload
    def get_user_by_id(
        self, user_id: int, *, as_objects: Literal[True]
    ) -> BlocketUser: ...

    @overload
    def get_user_by_id(
        self, user_id: int, *, as_objects: Literal[False] = False
    ) -> dict: ...

    @public_token
    def get_user_by_id(
        self, user_id: int, *, as_objects: bool = False
    ) -> dict | BlocketUser:
        """
        Returns a user's profile data. Contains account information, ads and more.
        Blocket url is https://www.blocket.se/profil/<user_id>.
        """
        url = f"{BASE_URL}/profile-be/v1/public-profiles/{user_id}"
        response = _make_request(url=f"{url}", token=self.token).json()
        return BlocketUser.model_validate(response) if as_objects else response

    @auth_token
    def save_ad(self, ad_id: int) -> dict:
        """
        Save an ad to "Saved ads" which can be found here:
        https://www.blocket.se/sparade/annonser
        """
        url = f"{BASE_URL}/search_bff/v1/saved_content/{ad_id}"
        response = _make_request(method=httpx.put, url=f"{url}", token=self.token)
        return {"status_code": response.status_code}

    @auth_token
    def get_saved_ads(self, limit: int = 100) -> dict:
        """
        Returns all of your saved ads from https://www.blocket.se/sparade/annonser.
        """
        url = f"{BASE_URL}/search_bff/v1/saved_content?lim={limit}"
        response = _make_request(url=f"{url}", token=self.token).json()
        return response

    @auth_token
    def get_threads(self, limit: int = 15) -> dict:
        """
        Returns set number of conversations/threads from Blocket, ordered by latest message.
        """
        assert self.token
        sendbird = Sendbird.generate(self.token)
        return sendbird.get_threads(limit=limit)

    @auth_token
    def get_messages_from_thread(self, channel_id: str) -> dict:
        """
        Returns all messages from a specific channel/thread.
        Requires a channel_id which can be found by using get_threads().
        Ex: sendbird_group_channel_12345_abc123abcde
        """
        assert self.token
        sendbird = Sendbird.generate(self.token)
        return sendbird.get_messages_from_thread(channel_id)

    @overload
    def unread_messages_count(
        self, *, as_objects: Literal[True]
    ) -> UnreadMessagesCount: ...

    @overload
    def unread_messages_count(self, *, as_objects: Literal[False] = False) -> dict: ...

    @auth_token
    def unread_messages_count(
        self, as_objects: bool = False
    ) -> dict | UnreadMessagesCount:
        """
        Returns the total count of unread messages.
        """
        assert self.token
        response = Sendbird.generate(self.token).unread_messages_count()
        return UnreadMessagesCount.model_validate(response) if as_objects else response
