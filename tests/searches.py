import respx
from httpx import Response
from blocket_api.blocket import BASE_URL, BlocketAPI, Category, Region, BYTBIL_URL
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
