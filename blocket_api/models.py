import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict

### CustomSearch ###


class _BaseModel(BaseModel):
    model_config = ConfigDict(extra="ignore")


class CustomSearchPrice(_BaseModel):
    suffix: str
    value: int


class CustomSearchLocation(_BaseModel):
    image_url: str
    label: str
    query_key: str | None = None


class CustomSearchImage(_BaseModel):
    height: int
    type: str
    url: str
    width: int


class CustomSearchCategory(_BaseModel):
    id: str
    name: str


class CustomSearchResult(_BaseModel):
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


class CustomSearchResults(_BaseModel):
    data: list[CustomSearchResult]
    total_count: int


### MotorSearch ###


class MotorSearchCarEquipment(_BaseModel):
    label: str


class MotorSearchCarLocation(_BaseModel):
    region: str
    municipality: str
    area: str


class MotorSearchCarImage(_BaseModel):
    height: int
    width: int
    image: str


class MotorSearchCar(_BaseModel):
    images: list[MotorSearchCarImage]
    location: MotorSearchCarLocation
    fuel: str
    gearbox: str
    regDate: int
    mileage: int
    equipment: list[MotorSearchCarEquipment] | None = None


class MotorSearchPrice(_BaseModel):
    amount: str
    billingPeriod: str
    oldPrice: str | None = None


class MotorSearchSeller(_BaseModel):
    type: str
    name: str
    id: str


class MotorSearchResult(_BaseModel):
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


class MotorSearchResults(_BaseModel):
    cars: list[MotorSearchResult]
    hits: int
    pages: int


### StoreSearch ###


class StoreSearchLocation(_BaseModel):
    longitude: float
    latitude: float


class StoreSearchImage(_BaseModel):
    height: int
    width: int
    url: str


class StoreSearchLogotype(_BaseModel):
    height: int
    width: int
    url: str


class StoreSearchResult(_BaseModel):
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


class StoreSearchResults(_BaseModel):
    data: list[StoreSearchResult]
    total_count: int
    total_page_count: int


### HomeSearch ###


class HomeSearchGeoPoint(_BaseModel):
    lat: float
    lon: float


class HomeSearchLocation(_BaseModel):
    id: int
    locality: str
    countryCode: str
    streetNumber: str | None = None
    point: HomeSearchGeoPoint
    route: str


class HomeSearchUpload(_BaseModel):
    id: int
    order: int | None = None
    type: str
    url: str


class HomeSearchResult(_BaseModel):
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


class Documents(_BaseModel):
    hasNextPage: bool
    hasPreviousPage: bool
    nodes: list[HomeSearchResult]
    pagesCount: int
    totalCount: int


class HomeIndexSearch(_BaseModel):
    documents: Documents


class DataModel(_BaseModel):
    homeIndexSearch: HomeIndexSearch


class HomeSearchResults(_BaseModel):
    data: DataModel


### StoreListings ###


class StoreListingContactMethods(_BaseModel):
    phone: bool


class StoreListingAdvertiser(_BaseModel):
    contact_methods: StoreListingContactMethods
    name: str
    store_name: str | None = None
    type: str


class StoreListingAttribute(_BaseModel):
    header: str
    id: str
    items: list[str]


class StoreListingCategory(_BaseModel):
    id: str
    name: str


class StoreListingImage(_BaseModel):
    height: int
    type: str
    url: str
    width: int


class StorListingLocationItem(_BaseModel):
    id: str
    name: str
    query_key: str


class StoreListingParameter(_BaseModel):
    id: str
    label: str
    value: str
    suffix: str | None = None


class ParameterGroup(_BaseModel):
    label: str
    parameters: list[StoreListingParameter]
    type: str


class StoreListingPartnerInfo(_BaseModel):
    external_id: str
    name: str


class StoreListingPrice(_BaseModel):
    suffix: str
    value: int


class StoreListing(_BaseModel):
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


class StoreListings(_BaseModel):
    data: list[StoreListing]


### GetAdById ###


class AdByIdReviews(_BaseModel):
    overall_score: int
    reviews_received_count: int


class AdByIdPublicProfile(_BaseModel):
    account_created_at: str
    badges: list[Any]
    blocket_account_id: str
    display_name: str
    number_of_active_ads: int
    reviews: AdByIdReviews
    verified: bool
    verified_label: str


class AdByIdContactMethods(_BaseModel):
    mc: bool


class AdByIdAdvertiser(_BaseModel):
    account_id: str
    contact_methods: AdByIdContactMethods
    name: str
    public_profile: AdByIdPublicProfile
    type: str


class AdByIdCategory(_BaseModel):
    id: str
    name: str


class AdByIdImage(_BaseModel):
    height: int
    type: str
    url: str
    width: int


class AdByIdLocation(_BaseModel):
    id: str
    name: str
    query_key: str


class AdByIdMap(_BaseModel):
    image_url: str
    label: str
    type: str


class AdByIdParameter(_BaseModel):
    id: str
    label: str
    value: str
    suffix: str | None = None


class AdByIdParameterGroup(_BaseModel):
    label: str
    parameters: list[AdByIdParameter]
    type: str


class AdByIdPrice(_BaseModel):
    suffix: str
    value: int


class AdByIdFeatures(_BaseModel):
    is_part_of_merge: bool


class AdByIdUrls(_BaseModel):
    seller_activate: str


class AdByIdBlocketPackage(_BaseModel):
    activated_providers: list[Any]
    ad_id: str
    blocket_payment_backwards_compatability: Any
    buyers_protection_fee: Any
    eligible_providers: list[Any]
    fail_code: Any
    failure: Any
    feature_swish: bool
    features: AdByIdFeatures
    is_in_dispute: bool
    partner: str
    payment_methods: list[Any]
    payment_request_entrance: Any
    payment_url: Any
    service_data: Any
    shipping_buy_now_entrance: Any
    state: str
    transaction_dates: Any
    urls: AdByIdUrls


class AdByIdGamApiKeywords(_BaseModel):
    adid: list[str]
    adtitle: list[str]
    adtype: list[str]
    appmode: list[str]
    blocket_section: list[str]
    companyad: list[str]
    country: list[str]
    country_code: list[str]
    county: list[str]
    id: list[str]
    itemimage: list[str]
    itemsecuredthumb: list[str]
    itemthumb: list[str]
    livingarea: list[str] | None = None
    lkf: list[str]
    municipality: list[str]
    nmp_vertical: list[str]
    page: list[str]
    price: list[str]
    price_range_2: list[str] | None = None
    publisher: list[str]
    services: list[Any]


class AdByIdClientKeywords(_BaseModel):
    cmp_advertising: str
    logged_in: str
    page_gen: str
    ppid_1: str
    ppid_2: str
    screen_height: str
    screen_width: str
    site_mode: str
    supply_type: str
    viewport_height: str
    viewport_width: str


class AdByIdGamContext(_BaseModel):
    api_keywords: AdByIdGamApiKeywords
    client_keywords: AdByIdClientKeywords


class AdByIdContext(_BaseModel):
    gam: AdByIdGamContext
    network_id: str | None = None


class AdByIdInventory(_BaseModel):
    context: AdByIdContext


class AdByIdGamKeywords(_BaseModel):
    adformat: list[str]
    adsize: list[str]


class AdByIdGamMediaType(_BaseModel):
    height: int | None = None
    type: str
    width: int | None = None


class AdByIdGamPlacement(_BaseModel):
    keywords: AdByIdGamKeywords
    media_types: list[AdByIdGamMediaType]
    path: str
    target_id: str


class AdByIdPlacement(_BaseModel):
    gam: AdByIdGamPlacement | None = None
    type: str
    vendor: str
    viewport: str
    safe_purchase: dict[str, Any] | None = None


class AdByIdData(_BaseModel):
    ad_id: str
    ad_status: str
    advertiser: AdByIdAdvertiser
    body: str
    category: list[AdByIdCategory]
    images: list[AdByIdImage]
    latitude: float | None = None
    list_id: str
    list_time: str
    location: list[AdByIdLocation]
    longitude: float | None = None
    map: AdByIdMap
    map_url: str
    parameter_groups: list[AdByIdParameterGroup]
    price: AdByIdPrice
    saved: bool
    share_url: str
    state_id: str
    subject: str
    type: str
    zipcode: str
    blocket_package: AdByIdBlocketPackage


class AdByIdResults(_BaseModel):
    data: AdByIdData
    inventory: AdByIdInventory
    placements: list[AdByIdPlacement] | None = None


### GetUserById ###


class BlocketUserAccount(_BaseModel):
    blocket_account_id: str
    created_at: datetime.datetime
    is_verified: bool
    name: str
    on_blocket_since: str
    verified_with: str


class BlocketUserAd(_BaseModel):
    ad_id: str
    ad_url: str
    image_url: str
    price: str
    region: str
    subject: str


class BlocketUserActiveAds(_BaseModel):
    ads: list[BlocketUserAd]
    label_primary: str
    label_secondary: str


class BlocketUserBadge(_BaseModel):
    description: str
    icon: str
    icon_blocket_ui: str
    id: str
    label: str


class BlocketUserCO2Savings(_BaseModel):
    date_range: str
    equivalent: str
    text: str


class BlocketUserProfileInfo(_BaseModel):
    description: str | None = None
    has_reviews: bool
    name: str


class BlocketUser(_BaseModel):
    account: BlocketUserAccount
    active_ads: BlocketUserActiveAds
    badges: list[BlocketUserBadge]
    co2_savings: BlocketUserCO2Savings
    profile_info: BlocketUserProfileInfo
    review_scores: dict | None = None


### SavedSearchesResult ###


class SavedSearch(_BaseModel):
    id: str
    name: str
    query: str
    total_count: int
    new_count: int
    push_enabled: bool
    push_available: bool
    email_enabled: bool | None = None


class SavedSearchResponse(_BaseModel):
    searches: list[SavedSearch]


## UnreadMessagesCount ##


class UnreadMessagesCount(_BaseModel):
    unread_count: int
