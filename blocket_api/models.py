import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class BlocketBaseModel(BaseModel):
    """Base model that allows unknown fields from the Blocket APIs."""

    model_config = ConfigDict(extra="allow")

### CustomSearch ###


class CustomSearchPrice(BaseModel):
    suffix: str
    value: int


class CustomSearchLocation(BaseModel):
    image_url: str
    label: str
    query_key: str | None = None


class CustomSearchImage(BaseModel):
    height: int
    type: str
    url: str
    width: int


class CustomSearchCategory(BaseModel):
    id: str
    name: str


class CustomSearchResult(BaseModel):
    ad_id: str
    ad_status: str
    body: str
    category: list[CustomSearchCategory]
    images: list[CustomSearchImage] = []
    list_id: str
    list_time: datetime.datetime
    map: CustomSearchLocation | None = None
    map_url: str | None = None
    price: CustomSearchPrice
    share_url: str
    state_id: str
    subject: str
    type: str
    zipcode: str | None = None


class CustomSearchResults(BaseModel):
    data: list[CustomSearchResult]
    total_count: int


### MotorSearch ###


class MotorSearchCarEquipment(BaseModel):
    label: str


class MotorSearchCarLocation(BaseModel):
    region: str
    municipality: str
    area: str


class MotorSearchCarImage(BaseModel):
    height: int
    width: int
    image: str


class MotorSearchCar(BaseModel):
    images: list[MotorSearchCarImage]
    location: MotorSearchCarLocation
    fuel: str
    gearbox: str
    regDate: int
    mileage: int
    equipment: list[MotorSearchCarEquipment] | None = None


class MotorSearchPrice(BaseModel):
    amount: str
    billingPeriod: str
    oldPrice: str | None = None


class MotorSearchSeller(BaseModel):
    type: str
    name: str
    id: str


class MotorSearchResult(BaseModel):
    dealId: str
    link: str
    listTime: datetime.datetime
    originalListTime: datetime.datetime
    seller: MotorSearchSeller
    heading: str
    price: MotorSearchPrice
    thumbnail: str
    car: MotorSearchCar
    description: str


class MotorSearchResults(BaseModel):
    cars: list[MotorSearchResult]
    hits: int
    pages: int


### StoreSearch ###


class StoreSearchLocation(BaseModel):
    longitude: float
    latitude: float


class StoreSearchImage(BaseModel):
    height: int
    width: int
    url: str


class StoreSearchLogotype(BaseModel):
    height: int
    width: int
    url: str


class StoreSearchResult(BaseModel):
    address: str | None = None
    id: str
    logotype: StoreSearchLogotype
    image: StoreSearchImage | None = None
    description: str
    external_store_url: str | None = None
    location: StoreSearchLocation | None = None
    name: str
    title: str
    ad_count: int
    category: str


class StoreSearchResults(BaseModel):
    data: list[StoreSearchResult]
    total_count: int
    total_page_count: int


### Saved searches ###


class SavedSearch(BlocketBaseModel):
    id: str
    name: str
    query: str | None = None
    new_count: int | None = None
    total_count: int | None = None
    push_enabled: bool | None = None
    push_available: bool | None = None


### Search content listings ###


class SearchContentPrice(BlocketBaseModel):
    value: Any | None = None
    suffix: str | None = None


class SearchContentAd(BlocketBaseModel):
    ad_id: str | None = None
    list_id: str | None = None
    subject: str | None = None
    body: str | None = None
    price: SearchContentPrice | None = None


class SearchContentResult(BlocketBaseModel):
    ad: SearchContentAd | None = None


class SearchContentResults(BlocketBaseModel):
    data: list[SearchContentResult]
    total_count: int | None = None
    total_page_count: int | None = None
    timestamp: datetime.datetime | None = None


### Price evaluation ###


class PriceEvaluation(BlocketBaseModel):
    registration_number: str | None = None
    private_valuation: int | None = None


### Home search ###


class HomeSearchPoint(BlocketBaseModel):
    lat: float | None = None
    lon: float | None = None


class HomeSearchLocation(BlocketBaseModel):
    id: str | None = None
    locality: str | None = None
    countryCode: str | None = None
    streetNumber: str | None = None
    route: str | None = None
    point: HomeSearchPoint | None = None


class HomeSearchUpload(BlocketBaseModel):
    id: str | None = None
    order: int | None = None
    type: str | None = None
    url: str | None = None


class HomeSearchDocument(BlocketBaseModel):
    id: str | None = None
    title: str | None = None
    bedroomCount: int | None = None
    roomCount: int | None = None
    rent: int | None = None
    currency: str | None = None
    monthlyCost: int | None = None
    homeType: str | None = None
    location: HomeSearchLocation | None = None
    uploads: list[HomeSearchUpload] | None = None


class HomeSearchDocuments(BlocketBaseModel):
    hasNextPage: bool | None = None
    hasPreviousPage: bool | None = None
    nodes: list[HomeSearchDocument] | None = None
    pagesCount: int | None = None
    totalCount: int | None = None


class HomeIndexSearch(BlocketBaseModel):
    documents: HomeSearchDocuments | None = None


class HomeSearchData(BlocketBaseModel):
    homeIndexSearch: HomeIndexSearch | None = None


class HomeSearchResponse(BlocketBaseModel):
    data: HomeSearchData | None = None
