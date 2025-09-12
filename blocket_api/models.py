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
