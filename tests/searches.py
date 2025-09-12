import datetime

import respx
from httpx import Response

from blocket_api.blocket import BASE_URL, BYTBIL_URL, BlocketAPI, Category, Region
from blocket_api.models import (
    CustomSearchImage,
    CustomSearchLocation,
    CustomSearchPrice,
    CustomSearchResult,
    CustomSearchResults,
    MotorSearchCar,
    MotorSearchCarEquipment,
    MotorSearchCarImage,
    MotorSearchCarLocation,
    MotorSearchPrice,
    MotorSearchResult,
    MotorSearchResults,
    MotorSearchSeller,
)
from blocket_api.qasa import QASA_URL, HomeType, OrderBy

api = BlocketAPI("token")


@respx.mock
def test_saved_searches() -> None:
    """
    Make sure mobility saved searches are merged with v2/searches.
    """
    respx.get(f"{BASE_URL}/saved/v2/searches").mock(
        return_value=Response(
            status_code=200,
            json={
                "data": [
                    {"id": "1", "name": '"buggy", Bilar säljes i hela Sverige'},
                    {"id": "2", "name": "Cyklar säljes i flera kommuner"},
                ],
            },
        ),
    )
    respx.get(f"{BASE_URL}/mobility-saved-searches/v1/searches").mock(
        return_value=Response(
            status_code=200,
            json={"data": [{"id": "3", "name": "Bilar säljes i hela Sverige"}]},
        ),
    )
    assert api.saved_searches() == [
        {"id": "1", "name": '"buggy", Bilar säljes i hela Sverige'},
        {"id": "2", "name": "Cyklar säljes i flera kommuner"},
        {"id": "3", "name": "Bilar säljes i hela Sverige"},
    ]


@respx.mock
def test_for_search_id() -> None:
    respx.get(f"{BASE_URL}/saved/v2/searches_content/123?lim=99").mock(
        return_value=Response(status_code=200, json={"data": "listings-data"}),
    )
    assert api.get_listings(search_id=123) == {"data": "listings-data"}


@respx.mock
def test_for_search_id_mobility() -> None:
    respx.get(f"{BASE_URL}/saved/v2/searches_content/123?lim=99").mock(
        return_value=Response(status_code=404),
    )
    respx.get(f"{BASE_URL}/mobility-saved-searches/v1/searches/123/ads?lim=99").mock(
        return_value=Response(status_code=200, json={"data": "mobility-data"}),
    )
    assert api.get_listings(search_id=123) == {"data": "mobility-data"}


class Test_CustomSearch:
    @respx.mock
    def test_custom_search(self) -> None:
        respx.get(
            f"{BASE_URL}/search_bff/v2/content?lim=99&q=saab&r=20&status=active"
        ).mock(
            return_value=Response(
                status_code=200, json={"data": {"location": "halland"}}
            ),
        )
        assert api.custom_search("saab", Region.halland) == {
            "data": {"location": "halland"}
        }

    @respx.mock
    def test_custom_search_as_objects(self) -> None:
        respx.get(
            f"{BASE_URL}/search_bff/v2/content?lim=99&q=saab&r=20&status=active"
        ).mock(
            return_value=Response(
                status_code=200,
                json={
                    "data": [
                        {
                            "ad_id": "ad_12345",
                            "ad_status": "active",
                            "body": "A nice car",
                            "category": [],
                            "images": [
                                {
                                    "height": 600,
                                    "type": "thumbnail",
                                    "url": "https://example.com/image1.jpg",
                                    "width": 800,
                                },
                            ],
                            "list_id": "list_9876",
                            "list_time": "2025-09-12T15:30:00Z",
                            "map": {
                                "image_url": "https://example.com/map.png",
                                "label": "Downtown",
                                "query_key": "loc_001",
                            },
                            "map_url": "https://maps.example.com/location?loc=001",
                            "price": {"suffix": "kr", "value": 2500},
                            "share_url": "https://example.com/share/ad_12345",
                            "state_id": "SE",
                            "subject": "Wow a car!",
                            "type": "rental",
                            "zipcode": "10001",
                        },
                    ],
                    "total_count": 1,
                },
            ),
        )
        result = api.custom_search("saab", Region.halland, as_objects=True)
        assert isinstance(result, CustomSearchResults)
        [data] = result.data

        assert data.ad_id == "ad_12345"
        assert data == CustomSearchResult(
            ad_id="ad_12345",
            ad_status="active",
            body="A nice car",
            category=[],
            images=[
                CustomSearchImage(
                    height=600,
                    type="thumbnail",
                    url="https://example.com/image1.jpg",
                    width=800,
                )
            ],
            list_id="list_9876",
            list_time=datetime.datetime(
                2025, 9, 12, 15, 30, tzinfo=datetime.timezone.utc
            ),
            map=CustomSearchLocation(
                image_url="https://example.com/map.png",
                label="Downtown",
                query_key="loc_001",
            ),
            map_url="https://maps.example.com/location?loc=001",
            price=CustomSearchPrice(suffix="kr", value=2500),
            share_url="https://example.com/share/ad_12345",
            state_id="SE",
            subject="Wow a car!",
            type="rental",
            zipcode="10001",
        )

    @respx.mock
    def test_custom_search_with_category(self) -> None:
        respx.get(
            f"{BASE_URL}/search_bff/v2/content?lim=99&q=saab&r=20&status=active&cg=2000"
        ).mock(
            return_value=Response(
                status_code=200,
                json={
                    "data": {
                        "location": "halland",
                        "category": Category.for_hemmet.value,
                    }
                },
            ),
        )
        result = api.custom_search(
            "saab", region=Region.halland, category=Category.for_hemmet
        )
        assert result == {
            "data": {"location": "halland", "category": Category.for_hemmet.value}
        }


class Test_MotorSearchURLs:
    @respx.mock
    def test_make_filter(self) -> None:
        expected_url_filter = '?filter={"key": "make", "values": ["Audi", "Toyota"]}'
        respx.get(
            f"{BASE_URL}/motor-search-service/v4/search/car{expected_url_filter}&page=1"
        ).mock(
            return_value=Response(status_code=200, json={"data": "ok"}),
        )
        assert api.motor_search(page=1, make=["Audi", "Toyota"]) == {"data": "ok"}

    @respx.mock
    def test_motor_search_as_objects(self) -> None:
        expected_url_filter = '?filter={"key": "make", "values": ["Audi", "Toyota"]}'
        respx.get(
            f"{BASE_URL}/motor-search-service/v4/search/car{expected_url_filter}&page=1"
        ).mock(
            return_value=Response(
                status_code=200,
                json={
                    "cars": [
                        {
                            "dealId": "deal_001",
                            "link": "https://example.com/car/001",
                            "listTime": "2025-09-12T14:00:00Z",
                            "originalListTime": "2025-09-10T09:00:00Z",
                            "seller": {
                                "type": "dealer",
                                "name": "Super Cars Ltd.",
                                "id": "seller_001",
                            },
                            "heading": "2020 BMW 3 Series 320i",
                            "price": {
                                "amount": "25000",
                                "billingPeriod": "one-time",
                                "oldPrice": None,
                            },
                            "thumbnail": "https://example.com/images/bmw_thumb.jpg",
                            "car": {
                                "images": [
                                    {
                                        "height": 800,
                                        "width": 1200,
                                        "image": "https://example.com/images/bmw1.jpg",
                                    },
                                    {
                                        "height": 600,
                                        "width": 900,
                                        "image": "https://example.com/images/bmw2.jpg",
                                    },
                                ],
                                "location": {
                                    "region": "SE",
                                    "municipality": "Stockholm",
                                    "area": "Downtown",
                                },
                                "fuel": "Petrol",
                                "gearbox": "Automatic",
                                "regDate": 2020,
                                "mileage": 15000,
                                "equipment": [
                                    {"label": "Air Conditioning"},
                                    {"label": "GPS Navigation"},
                                    {"label": "Heated Seats"},
                                ],
                            },
                            "description": "A nice car, yea?",
                        },
                    ],
                    "hits": 1,
                    "pages": 1,
                },
            ),
        )
        result = api.motor_search(page=1, make=["Audi", "Toyota"], as_objects=True)
        assert isinstance(result, MotorSearchResults)

        [car_ad] = result.cars
        assert car_ad == MotorSearchResult(
            dealId="deal_001",
            link="https://example.com/car/001",
            listTime=datetime.datetime(
                2025, 9, 12, 14, 0, tzinfo=datetime.timezone.utc
            ),
            originalListTime=datetime.datetime(
                2025, 9, 10, 9, 0, tzinfo=datetime.timezone.utc
            ),
            seller=MotorSearchSeller(
                type="dealer", name="Super Cars Ltd.", id="seller_001"
            ),
            heading="2020 BMW 3 Series 320i",
            price=MotorSearchPrice(
                amount="25000", billingPeriod="one-time", oldPrice=None
            ),
            thumbnail="https://example.com/images/bmw_thumb.jpg",
            car=MotorSearchCar(
                images=[
                    MotorSearchCarImage(
                        height=800,
                        width=1200,
                        image="https://example.com/images/bmw1.jpg",
                    ),
                    MotorSearchCarImage(
                        height=600,
                        width=900,
                        image="https://example.com/images/bmw2.jpg",
                    ),
                ],
                location=MotorSearchCarLocation(
                    region="SE", municipality="Stockholm", area="Downtown"
                ),
                fuel="Petrol",
                gearbox="Automatic",
                regDate=2020,
                mileage=15000,
                equipment=[
                    MotorSearchCarEquipment(label="Air Conditioning"),
                    MotorSearchCarEquipment(label="GPS Navigation"),
                    MotorSearchCarEquipment(label="Heated Seats"),
                ],
            ),
            description="A nice car, yea?",
        )

    @respx.mock
    def test_range_filters(self) -> None:
        expected_url_filter = (
            '?filter={"key": "make", "values": ["Ford"]}'
            '&filter={"key": "price", "range": {"start": "1000", "end": "2000"}}'
            '&filter={"key": "modelYear", "range": {"start": "1995", "end": "2000"}}'
            '&filter={"key": "milage", "range": {"start": "1000", "end": "5000"}}'
            '&filter={"key": "gearbox", "values": "Manuell"}'
        )
        respx.get(
            f"{BASE_URL}/motor-search-service/v4/search/car{expected_url_filter}&page=5"
        ).mock(
            return_value=Response(status_code=200, json={"data": "ok"}),
        )
        assert api.motor_search(
            page=5,
            make=["Ford"],
            price=(1000, 2000),
            modelYear=(1995, 2000),
            milage=(1000, 5000),
            gearbox="Manuell",
        ) == {"data": "ok"}


@respx.mock
def test_price_eval() -> None:
    respx.get(f"{BYTBIL_URL}/blocket-basedata-api/v3/vehicle-data/ABC123").mock(
        return_value=Response(
            status_code=200,
            json={
                "registration_number": "ABC123",
                "private_valuation": 108155,
            },
        ),
    )
    assert api.price_eval("ABC123") == {
        "registration_number": "ABC123",
        "private_valuation": 108155,
    }


@respx.mock
def test_home_search() -> None:
    respx.post(f"{QASA_URL}").mock(
        return_value=Response(
            status_code=200,
            json={
                "bedroomCount": "2",
                "rent": 9500,
                "petsAllowed": False,
            },
        ),
    )
    assert api.home_search(
        city="Stockholm",
        type=HomeType.apartment,
        order_by=OrderBy.price,
    ) == {
        "bedroomCount": "2",
        "rent": 9500,
        "petsAllowed": False,
    }


class Test_StoreSearch:
    @respx.mock
    def test_search_store(self) -> None:
        respx.get(f"{BASE_URL}/search_bff/v1/stores?q=bilar&page=0").mock(
            return_value=Response(
                status_code=200,
                json={"data": {"store_id": 1234, "store_name": "Bilar AB"}},
            ),
        )
        assert api.search_store("bilar") == {
            "data": {"store_id": 1234, "store_name": "Bilar AB"}
        }

    @respx.mock
    def test_get_store_listings(self) -> None:
        respx.get(
            f"{BASE_URL}/search_bff/v2/content?lim=60&page=0&sort=rel"
            "&store_id=1234&status=active&gl=3&include=extend_with_shipping"
        ).mock(
            return_value=Response(
                status_code=200,
                json={"data": {"ad_id": 1234, "body": "A good car"}},
            ),
        )
        assert api.get_store_listings(1234) == {
            "data": {"ad_id": 1234, "body": "A good car"}
        }
