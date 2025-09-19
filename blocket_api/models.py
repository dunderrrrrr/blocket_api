import datetime

from pydantic import BaseModel, ConfigDict

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


### SavedSearch ###


class SavedSearch(BaseModel):
    id: str
    name: str | None = None
    query: str | None = None
    new_count: int | None = None
    total_count: int | None = None
    push_enabled: bool | None = None
    push_available: bool | None = None

    model_config = ConfigDict(extra="allow")


### Listings ###


class ListingPrice(BaseModel):
    value: int | float | None = None
    suffix: str | None = None

    model_config = ConfigDict(extra="allow")


class ListingAd(BaseModel):
    ad_id: str | None = None
    ad_status: str | None = None
    body: str | None = None
    list_id: str | None = None
    list_time: datetime.datetime | None = None
    subject: str | None = None
    zipcode: str | None = None
    price: ListingPrice | None = None

    model_config = ConfigDict(extra="allow")


class ListingEntry(BaseModel):
    ad: ListingAd | None = None

    model_config = ConfigDict(extra="allow")


class ListingResults(BaseModel):
    data: list[ListingEntry]
    total_count: int | None = None
    timestamp: datetime.datetime | None = None
    total_page_count: int | None = None

    model_config = ConfigDict(extra="allow")


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


### Price evaluation ###


class PriceEvaluation(BaseModel):
    registration_number: str
    private_valuation: int | None = None

    model_config = ConfigDict(extra="allow")


### Home search ###


class HomeSearchUpload(BaseModel):
    id: str | None = None
    order: int | None = None
    type: str | None = None
    url: str | None = None

    model_config = ConfigDict(extra="allow")


class HomeSearchLocationPoint(BaseModel):
    lat: float | None = None
    lon: float | None = None

    model_config = ConfigDict(extra="allow")


class HomeSearchLocation(BaseModel):
    id: str | None = None
    locality: str | None = None
    countryCode: str | None = None
    streetNumber: str | None = None
    point: HomeSearchLocationPoint | None = None
    route: str | None = None

    model_config = ConfigDict(extra="allow")


class HomeSearchNode(BaseModel):
    bedroomCount: int | None = None
    blockListing: bool | None = None
    rentalLengthSeconds: int | None = None
    householdSize: int | None = None
    corporateHome: bool | None = None
    description: str | None = None
    endDate: datetime.datetime | None = None
    firstHand: bool | None = None
    furnished: bool | None = None
    homeType: str | None = None
    id: str | None = None
    instantSign: bool | None = None
    market: str | None = None
    lastBumpedAt: datetime.datetime | None = None
    monthlyCost: int | None = None
    petsAllowed: bool | None = None
    platform: str | None = None
    publishedAt: datetime.datetime | None = None
    publishedOrBumpedAt: datetime.datetime | None = None
    earlyAccessEndsAt: datetime.datetime | None = None
    rent: int | None = None
    currency: str | None = None
    roomCount: int | None = None
    seniorHome: bool | None = None
    shared: bool | None = None
    shortcutHome: bool | None = None
    smokingAllowed: bool | None = None
    sortingScore: float | None = None
    squareMeters: int | None = None
    startDate: datetime.datetime | None = None
    studentHome: bool | None = None
    tenantBaseFee: int | None = None
    title: str | None = None
    wheelchairAccessible: bool | None = None
    location: HomeSearchLocation | None = None
    displayStreetNumber: str | None = None
    uploads: list[HomeSearchUpload] | None = None

    model_config = ConfigDict(extra="allow")


class HomeSearchDocuments(BaseModel):
    hasNextPage: bool | None = None
    hasPreviousPage: bool | None = None
    nodes: list[HomeSearchNode] | None = None
    pagesCount: int | None = None
    totalCount: int | None = None

    model_config = ConfigDict(extra="allow")


class HomeIndexSearch(BaseModel):
    documents: HomeSearchDocuments | None = None

    model_config = ConfigDict(extra="allow")


class HomeSearchData(BaseModel):
    homeIndexSearch: HomeIndexSearch | None = None

    model_config = ConfigDict(extra="allow")


class HomeSearchResponse(BaseModel):
    data: HomeSearchData | None = None
    errors: list[dict] | None = None

    model_config = ConfigDict(extra="allow")
