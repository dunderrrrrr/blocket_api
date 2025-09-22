import datetime

from pydantic import BaseModel

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


### HomeSearch ###


class HomeSearchGeoPoint(BaseModel):
    lat: float
    lon: float


class HomeSearchLocation(BaseModel):
    id: int
    locality: str
    countryCode: str
    streetNumber: str | None = None
    point: HomeSearchGeoPoint
    route: str


class HomeSearchUpload(BaseModel):
    id: int
    order: int | None = None
    type: str
    url: str


class HomeSearchResult(BaseModel):
    bedroomCount: int | None = None
    blockListing: bool
    rentalLengthSeconds: float | None = None
    householdSize: int
    corporateHome: bool
    description: str
    endDate: str | None = None
    firstHand: bool
    furnished: bool
    homeType: str
    id: str
    instantSign: bool
    market: str
    lastBumpedAt: str | None = None
    monthlyCost: int
    petsAllowed: bool
    platform: str
    publishedAt: str
    publishedOrBumpedAt: str
    earlyAccessEndsAt: str | None = None
    rent: int
    currency: str
    roomCount: int
    seniorHome: bool
    shared: bool
    shortcutHome: bool
    smokingAllowed: bool
    sortingScore: float
    squareMeters: int
    startDate: str
    studentHome: bool
    tenantBaseFee: int
    title: str | None = None
    wheelchairAccessible: bool
    location: HomeSearchLocation
    displayStreetNumber: bool
    uploads: list[HomeSearchUpload]


class Documents(BaseModel):
    hasNextPage: bool
    hasPreviousPage: bool
    nodes: list[HomeSearchResult]
    pagesCount: int
    totalCount: int


class HomeIndexSearch(BaseModel):
    documents: Documents


class DataModel(BaseModel):
    homeIndexSearch: HomeIndexSearch


class HomeSearchResults(BaseModel):
    data: DataModel


### StoreListings ###


class StoreListingContactMethods(BaseModel):
    phone: bool


class StoreListingAdvertiser(BaseModel):
    contact_methods: StoreListingContactMethods
    name: str
    store_name: str | None = None
    type: str


class StoreListingAttribute(BaseModel):
    header: str
    id: str
    items: list[str]


class StoreListingCategory(BaseModel):
    id: str
    name: str


class StoreListingImage(BaseModel):
    height: int
    type: str
    url: str
    width: int


class StorListingLocationItem(BaseModel):
    id: str
    name: str
    query_key: str


class StoreListingParameter(BaseModel):
    id: str
    label: str
    value: str
    suffix: str | None = None


class ParameterGroup(BaseModel):
    label: str
    parameters: list[StoreListingParameter]
    type: str


class StoreListingPartnerInfo(BaseModel):
    external_id: str
    name: str


class StoreListingPrice(BaseModel):
    suffix: str
    value: int


class StoreListing(BaseModel):
    ad_id: str
    ad_status: str
    advertiser: StoreListingAdvertiser
    attributes: list[StoreListingAttribute]
    body: str
    category: list[StoreListingCategory]
    images: list[StoreListingImage]
    license_plate: str | None = None
    list_id: str
    list_time: str
    location: list[StorListingLocationItem]
    map_url: str | None = None
    parameter_groups: list[ParameterGroup]
    partner_info: StoreListingPartnerInfo
    price: StoreListingPrice
    share_url: str
    state_id: str
    subject: str
    type: str


class StoreListings(BaseModel):
    data: list[StoreListing]
