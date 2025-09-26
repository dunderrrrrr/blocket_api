import datetime

import respx
from httpx import Response

from blocket_api.blocket import BASE_URL, BYTBIL_URL, BlocketAPI, Category, Region
from blocket_api.models import (
    AdByIdAdvertiser,
    AdByIdBlocketPackage,
    AdByIdCategory,
    AdByIdClientKeywords,
    AdByIdContactMethods,
    AdByIdContext,
    AdByIdData,
    AdByIdFeatures,
    AdByIdGamApiKeywords,
    AdByIdGamContext,
    AdByIdImage,
    AdByIdInventory,
    AdByIdLocation,
    AdByIdMap,
    AdByIdParameter,
    AdByIdParameterGroup,
    AdByIdPrice,
    AdByIdPublicProfile,
    AdByIdResults,
    AdByIdReviews,
    AdByIdUrls,
    BlocketUser,
    BlocketUserAccount,
    BlocketUserActiveAds,
    BlocketUserAd,
    BlocketUserBadge,
    BlocketUserCO2Savings,
    BlocketUserProfileInfo,
    CustomSearchImage,
    CustomSearchLocation,
    CustomSearchPrice,
    CustomSearchResult,
    CustomSearchResults,
    DataModel,
    Documents,
    HomeIndexSearch,
    HomeSearchGeoPoint,
    HomeSearchLocation,
    HomeSearchResult,
    HomeSearchResults,
    HomeSearchUpload,
    MotorSearchCar,
    MotorSearchCarEquipment,
    MotorSearchCarImage,
    MotorSearchCarLocation,
    MotorSearchPrice,
    MotorSearchResult,
    MotorSearchResults,
    MotorSearchSeller,
    ParameterGroup,
    StoreListing,
    StoreListingAdvertiser,
    StoreListingAttribute,
    StoreListingCategory,
    StoreListingContactMethods,
    StoreListingImage,
    StoreListingParameter,
    StoreListingPartnerInfo,
    StoreListingPrice,
    StoreListings,
    StorListingLocationItem,
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


class Test_HomeSearch:
    @respx.mock
    def test_home_search(self) -> None:
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

    @respx.mock
    def test_home_search_as_objects(self) -> None:
        respx.post(f"{QASA_URL}").mock(
            return_value=Response(
                status_code=200,
                json={
                    "data": {
                        "homeIndexSearch": {
                            "documents": {
                                "hasNextPage": True,
                                "hasPreviousPage": False,
                                "nodes": [
                                    {
                                        "bedroomCount": None,
                                        "blockListing": False,
                                        "rentalLengthSeconds": None,
                                        "householdSize": 2,
                                        "corporateHome": False,
                                        "description": "Charmig och rymlig 1:a med stor balkong",
                                        "endDate": None,
                                        "firstHand": False,
                                        "furnished": True,
                                        "homeType": "apartment",
                                        "id": "1205500",
                                        "instantSign": False,
                                        "market": "sweden",
                                        "lastBumpedAt": None,
                                        "monthlyCost": 12184,
                                        "petsAllowed": False,
                                        "platform": "qasa",
                                        "publishedAt": "2025-09-22T16:20:08Z",
                                        "publishedOrBumpedAt": "2025-09-22T16:20:08Z",
                                        "earlyAccessEndsAt": None,
                                        "rent": 11500,
                                        "currency": "SEK",
                                        "roomCount": 1,
                                        "seniorHome": False,
                                        "shared": False,
                                        "shortcutHome": False,
                                        "smokingAllowed": False,
                                        "sortingScore": 8.351962081128748,
                                        "squareMeters": 33,
                                        "startDate": "2025-11-01T00:00:00+00:00",
                                        "studentHome": False,
                                        "tenantBaseFee": 684,
                                        "title": None,
                                        "wheelchairAccessible": False,
                                        "location": {
                                            "id": 3137542,
                                            "locality": "Bromma",
                                            "countryCode": "SE",
                                            "streetNumber": None,
                                            "point": {
                                                "lat": 1.338915,
                                                "lon": 1.9352853,
                                                "__typename": "GeoPoint",
                                            },
                                            "route": "Snörmakarvägen",
                                            "__typename": "HomeDocumentLocationType",
                                        },
                                        "displayStreetNumber": False,
                                        "uploads": [
                                            {
                                                "id": 17216695,
                                                "order": 11,
                                                "type": "home_picture",
                                                "url": "https://image.here/image.jpg",
                                                "__typename": "HomeDocumentUploadType",
                                            },
                                        ],
                                        "__typename": "HomeDocument",
                                    }
                                ],
                                "pagesCount": 25,
                                "totalCount": 1442,
                                "__typename": "HomeDocumentOffsetLimit",
                            },
                            "__typename": "HomeIndexSearchQuery",
                        }
                    }
                },
            ),
        )
        assert api.home_search(
            city="Stockholm", type=HomeType.apartment, as_objects=True
        ) == HomeSearchResults(
            data=DataModel(
                homeIndexSearch=HomeIndexSearch(
                    documents=Documents(
                        hasNextPage=True,
                        hasPreviousPage=False,
                        nodes=[
                            HomeSearchResult(
                                bedroomCount=None,
                                blockListing=False,
                                rentalLengthSeconds=None,
                                householdSize=2,
                                corporateHome=False,
                                description="Charmig och rymlig 1:a med stor balkong",
                                endDate=None,
                                firstHand=False,
                                furnished=True,
                                homeType="apartment",
                                id="1205500",
                                instantSign=False,
                                market="sweden",
                                lastBumpedAt=None,
                                monthlyCost=12184,
                                petsAllowed=False,
                                platform="qasa",
                                publishedAt="2025-09-22T16:20:08Z",
                                publishedOrBumpedAt="2025-09-22T16:20:08Z",
                                earlyAccessEndsAt=None,
                                rent=11500,
                                currency="SEK",
                                roomCount=1,
                                seniorHome=False,
                                shared=False,
                                shortcutHome=False,
                                smokingAllowed=False,
                                sortingScore=8.351962081128748,
                                squareMeters=33,
                                startDate="2025-11-01T00:00:00+00:00",
                                studentHome=False,
                                tenantBaseFee=684,
                                title=None,
                                wheelchairAccessible=False,
                                location=HomeSearchLocation(
                                    id=3137542,
                                    locality="Bromma",
                                    countryCode="SE",
                                    streetNumber=None,
                                    point=HomeSearchGeoPoint(
                                        lat=1.338915, lon=1.9352853
                                    ),
                                    route="Snörmakarvägen",
                                ),
                                displayStreetNumber=False,
                                uploads=[
                                    HomeSearchUpload(
                                        id=17216695,
                                        order=11,
                                        type="home_picture",
                                        url="https://image.here/image.jpg",
                                    )
                                ],
                            )
                        ],
                        pagesCount=25,
                        totalCount=1442,
                    )
                )
            )
        )


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

    @respx.mock
    def test_get_store_listings_as_objects(self) -> None:
        respx.get(
            f"{BASE_URL}/search_bff/v2/content?lim=60&page=0&sort=rel"
            "&store_id=1234&status=active&gl=3&include=extend_with_shipping"
        ).mock(
            return_value=Response(
                status_code=200,
                json={
                    "data": [
                        {
                            "ad_id": "1001970418",
                            "ad_status": "active",
                            "advertiser": {
                                "contact_methods": {"phone": True},
                                "name": "Riddermark Bil – Megastore",
                                "store_name": "Riddermark Bil – Megastore",
                                "type": "store",
                            },
                            "attributes": [
                                {
                                    "header": "Utrustning",
                                    "id": "car_equipment",
                                    "items": [
                                        "ST-Line",
                                        "Backkamera",
                                        "Parkeringssensorer bak",
                                        "Multifunktionsratt",
                                        "Farthållare",
                                        "Växelpaddlar/Rattpaddlar",
                                        "Keyless Start",
                                        "Bluetooth",
                                        "2-Zons klimatanläggning",
                                        "ACC/Klimatanläggning",
                                        "Sätesvärme fram",
                                        "Tonade rutor",
                                        "12V-uttag",
                                        "Svensksåld",
                                    ],
                                }
                            ],
                            "body": "A body here",
                            "category": [
                                {"id": "1000", "name": "Fordon"},
                                {"id": "1020", "name": "Bilar"},
                            ],
                            "images": [
                                {
                                    "height": 1333,
                                    "type": "image",
                                    "url": "https://i.blocketcdn.se/pictures/asl/1001970418/0997962324.jpg",
                                    "width": 2000,
                                },
                            ],
                            "license_plate": "PJD337",
                            "list_id": "1001970418",
                            "list_time": "2025-09-22T19:05:59+02:00",
                            "location": [
                                {"id": "12", "name": "Södermanland", "query_key": "r"},
                                {"id": "148", "name": "Strängnäs", "query_key": "m"},
                            ],
                            "map_url": "https://www.hitta.se/kartan/partner/blocketv2?ad_id=1001970418",
                            "parameter_groups": [
                                {
                                    "label": "Allmän information",
                                    "parameters": [
                                        {
                                            "id": "fuel",
                                            "label": "Bränsle",
                                            "value": "Bensin",
                                        },
                                        {
                                            "id": "gearbox",
                                            "label": "Växellåda",
                                            "value": "Automat",
                                        },
                                        {
                                            "id": "mileage",
                                            "label": "Miltal",
                                            "value": "6\xa0253",
                                        },
                                        {
                                            "id": "regdate",
                                            "label": "Modellår",
                                            "value": "2017",
                                        },
                                    ],
                                    "type": "general",
                                },
                                {
                                    "label": "Information från BytBil",
                                    "parameters": [
                                        {
                                            "id": "cx_make",
                                            "label": "Märke",
                                            "value": "Ford",
                                        },
                                    ],
                                    "type": "car",
                                },
                            ],
                            "partner_info": {
                                "external_id": "18044171",
                                "name": "bytbil",
                            },
                            "price": {"suffix": "kr", "value": 149800},
                            "share_url": "https://www.blocket.se/annons/sodermanland/ford_focus_kombi_ecoboost_125hk_st_line_kamera_farthallare_/1001970418",
                            "state_id": "819",
                            "subject": "Ford Focus Kombi EcoBoost 125hk ST-Line Kamera Farthållare *",
                            "type": "s",
                        }
                    ]
                },
            ),
        )
        assert api.get_store_listings(1234, as_objects=True) == StoreListings(
            data=[
                StoreListing(
                    ad_id="1001970418",
                    ad_status="active",
                    advertiser=StoreListingAdvertiser(
                        contact_methods=StoreListingContactMethods(phone=True),
                        name="Riddermark Bil – Megastore",
                        store_name="Riddermark Bil – Megastore",
                        type="store",
                    ),
                    attributes=[
                        StoreListingAttribute(
                            header="Utrustning",
                            id="car_equipment",
                            items=[
                                "ST-Line",
                                "Backkamera",
                                "Parkeringssensorer bak",
                                "Multifunktionsratt",
                                "Farthållare",
                                "Växelpaddlar/Rattpaddlar",
                                "Keyless Start",
                                "Bluetooth",
                                "2-Zons klimatanläggning",
                                "ACC/Klimatanläggning",
                                "Sätesvärme fram",
                                "Tonade rutor",
                                "12V-uttag",
                                "Svensksåld",
                            ],
                        )
                    ],
                    body="A body here",
                    category=[
                        StoreListingCategory(id="1000", name="Fordon"),
                        StoreListingCategory(id="1020", name="Bilar"),
                    ],
                    images=[
                        StoreListingImage(
                            height=1333,
                            type="image",
                            url="https://i.blocketcdn.se/pictures/asl/1001970418/0997962324.jpg",
                            width=2000,
                        )
                    ],
                    license_plate="PJD337",
                    list_id="1001970418",
                    list_time="2025-09-22T19:05:59+02:00",
                    location=[
                        StorListingLocationItem(
                            id="12", name="Södermanland", query_key="r"
                        ),
                        StorListingLocationItem(
                            id="148", name="Strängnäs", query_key="m"
                        ),
                    ],
                    map_url="https://www.hitta.se/kartan/partner/blocketv2?ad_id=1001970418",
                    parameter_groups=[
                        ParameterGroup(
                            label="Allmän information",
                            parameters=[
                                StoreListingParameter(
                                    id="fuel",
                                    label="Bränsle",
                                    value="Bensin",
                                    suffix=None,
                                ),
                                StoreListingParameter(
                                    id="gearbox",
                                    label="Växellåda",
                                    value="Automat",
                                    suffix=None,
                                ),
                                StoreListingParameter(
                                    id="mileage",
                                    label="Miltal",
                                    value="6\xa0253",
                                    suffix=None,
                                ),
                                StoreListingParameter(
                                    id="regdate",
                                    label="Modellår",
                                    value="2017",
                                    suffix=None,
                                ),
                            ],
                            type="general",
                        ),
                        ParameterGroup(
                            label="Information från BytBil",
                            parameters=[
                                StoreListingParameter(
                                    id="cx_make",
                                    label="Märke",
                                    value="Ford",
                                    suffix=None,
                                )
                            ],
                            type="car",
                        ),
                    ],
                    partner_info=StoreListingPartnerInfo(
                        external_id="18044171", name="bytbil"
                    ),
                    price=StoreListingPrice(suffix="kr", value=149800),
                    share_url="https://www.blocket.se/annons/sodermanland/ford_focus_kombi_ecoboost_125hk_st_line_kamera_farthallare_/1001970418",
                    state_id="819",
                    subject="Ford Focus Kombi EcoBoost 125hk ST-Line Kamera Farthållare *",
                    type="s",
                )
            ]
        )


class Test_GetAdById:
    @respx.mock
    def test_get_ad_by_id(self) -> None:
        respx.get(f"{BASE_URL}/search_bff/v2/content/1213640595").mock(
            return_value=Response(
                status_code=200,
                json={"data": {"ad_id": 1213640595, "title": "A nice ad."}},
            ),
        )
        assert api.get_ad_by_id(1213640595) == {
            "data": {"ad_id": 1213640595, "title": "A nice ad."}
        }

    @respx.mock
    def test_get_ad_by_id_as_objects(self) -> None:
        respx.get(f"{BASE_URL}/search_bff/v2/content/1213640595").mock(
            return_value=Response(
                status_code=200,
                json={
                    "data": {
                        "ad_id": "1213640595",
                        "ad_status": "active",
                        "advertiser": {
                            "account_id": "2691672",
                            "contact_methods": {"mc": True},
                            "name": "Växjö",
                            "public_profile": {
                                "account_created_at": "2016-04-30T08:07:49.607Z",
                                "badges": [
                                    {
                                        "description": "405 annonser inom 6 mån",
                                        "icon_bui": "IconMedalMulticolor",
                                        "icon_src": "https://public-assets.blocketcdn.se/static/icons/medal.png",
                                        "id": "active-user",
                                        "label": "Aktiv på Blocket",
                                    },
                                ],
                                "blocket_account_id": "1223",
                                "display_name": "Växjö",
                                "number_of_active_ads": 136,
                                "reviews": {
                                    "overall_score": 97,
                                    "reviews_received_count": 39,
                                    "worded_overall_score": "Perfekt",
                                },
                                "verified": True,
                                "verified_label": "BankID",
                            },
                            "type": "private",
                        },
                        "body": "A nice body!",
                        "category": [
                            {"id": "4000", "name": "Personligt"},
                            {"id": "4080", "name": "Kläder & skor"},
                        ],
                        "co2_text": "Denna vara sparar 17 kg CO₂e vilket motsvarar produktionen av 87 nya plastpåsar.",
                        "images": [
                            {
                                "height": 1024,
                                "type": "image",
                                "url": "https://i.blocketcdn.se/pictures/recommerce/1213640595/fe21cc7b-8613-4f7f-846a-67d86fe0dcb9.jpg",
                                "width": 768,
                            },
                        ],
                        "list_id": "1213640595",
                        "list_time": "2025-09-23T18:48:34+02:00",
                        "location": [
                            {"id": "21", "name": "Kronoberg", "query_key": "r"},
                            {"id": "251", "name": "Växjö", "query_key": "m"},
                        ],
                        "map": {
                            "image_url": "https://api.hitta.se/image/v2/0/15?location=%7B%22zip%22:%2235244%22%7D&zoom.to=location",
                            "label": "352 44 Växjö, Kronobergs län",
                            "type": "zipcode",
                        },
                        "map_url": "https://www.hitta.se/kartan/partner/blocketv2?ad_id=1213640595",
                        "parameter_groups": [
                            {
                                "label": "Allmän information",
                                "parameters": [
                                    {
                                        "id": "item_condition",
                                        "label": "Skick",
                                        "short_value": "Bra skick",
                                        "value": "Bra skick - Sparsamt använd",
                                    }
                                ],
                                "type": "general",
                            },
                            {
                                "label": "Mer om kläderna",
                                "parameters": [
                                    {
                                        "id": "clothing_kind",
                                        "label": "Typ av plagg",
                                        "value": "Jackor & ytterplagg",
                                    },
                                ],
                                "type": "clothing",
                            },
                        ],
                        "parameters_raw": {
                            "is_shipping_buy_now_enabled": {"value": "1"},
                            "shipping_enabled": {"value": "1"},
                        },
                        "price": {"suffix": "kr", "value": 1100},
                        "price_badge": {
                            "icon": {
                                "url": "https://public-assets.blocketcdn.se/static/icons/shipping-buyer-protection.png"
                            },
                            "id": "shipping_enabled",
                            "label": "Köp nu",
                        },
                        "saved": False,
                        "share_url": "https://www.blocket.se/annons/kronoberg/ralph_lauren_rock_herrock_hostjacka_herrjacka_herr_s/1213640595",
                        "state_id": "830afc45-ecfa-4ce7-b400-07736a7a4fcb",
                        "subject": "Ralph Lauren Rock herrock höstjacka herrjacka Herr S",
                        "type": "s",
                        "zipcode": "35244",
                        "blocket_package": {
                            "activated_providers": [
                                {
                                    "cost": 126,
                                    "id": "d9f6c92d-0b18-4bb5-b5cf-479227a8239c",
                                }
                            ],
                            "ad_id": "1213640595",
                            "blocket_payment_backwards_compatability": None,
                            "buyers_protection_fee": 77,
                            "eligible_providers": [
                                {"id": "d9f6c92d-0b18-4bb5-b5cf-479227a8239c"}
                            ],
                            "fail_code": None,
                            "failure": None,
                            "feature_swish": True,
                            "features": {
                                "bank_id_type": "rocker-without-ssn",
                                "is_native_purchase_flow": True,
                                "is_part_of_merge": True,
                                "is_status_page_redirect_to_survey_enabled": False,
                                "should_get_new_web_when_activating": True,
                                "swish_payout": True,
                            },
                            "is_in_dispute": False,
                            "partner": "other",
                            "payment_methods": [
                                {
                                    "id": "mastercard",
                                    "label": "Mastercard",
                                    "src_dark": "https://public-assets.blocketcdn.se/static/icons/payment-methods/mastercard_dark.png",
                                    "src_light": "https://public-assets.blocketcdn.se/static/icons/payment-methods/mastercard.png",
                                },
                            ],
                            "payment_request_entrance": {
                                "icon": {
                                    "id": "icon_shipping_payment_request_secondary",
                                    "label": "Skicka prisförslag",
                                    "src_dark": "https://public-assets.blocketcdn.se/static/icons/buy-now-for-shipping/shipping_icon_primary.png",
                                    "src_light": "https://public-assets.blocketcdn.se/static/icons/buy-now-for-shipping/shipping_icon_secondary.png",
                                },
                                "info_text": None,
                                "is_enabled": True,
                                "link": None,
                                "text": "Skicka prisförslag",
                                "url": "https://www.blocket.se/frakt/kopare-knapp?ad_id=1213640595&partner=other&source=ad&seller_blocket_account_id=2691672",
                            },
                            "payment_url": None,
                            "service_data": {
                                "information": {
                                    "content": [
                                        {
                                            "bullet_points": [
                                                "Godkänn varan innan säljaren får betalt",
                                                "Hjälp om varan behöver reklameras",
                                                "Klimatkompenserad frakt med förväntad leveranstid på 1-2 vardagar",
                                            ],
                                            "info_text": "Köpskyddet är baserat på varans pris.",
                                            "links": [
                                                {
                                                    "text": "Så funkar frakt med köpskydd",
                                                    "url": "https://www.blocket.se/om-kopskydd?hideui=1",
                                                }
                                            ],
                                            "price_points": [
                                                {
                                                    "campaign_text": None,
                                                    "icon_url": "https://public-assets.blocketcdn.se/static/icons/buyers-protection-fee/shipping_icon.png",
                                                    "icon_url_dark": "https://public-assets.blocketcdn.se/static/icons/buyers-protection-fee/shipping_icon_dark_mode.png",
                                                    "original_price": 49,
                                                    "price": 49,
                                                    "text": "DB Schenker 49 kr",
                                                },
                                                {
                                                    "campaign_text": None,
                                                    "icon_url": "https://public-assets.blocketcdn.se/static/icons/buyers-protection-fee/plus.png",
                                                    "icon_url_dark": "https://public-assets.blocketcdn.se/static/icons/buyers-protection-fee/plus_dark_mode.png",
                                                    "original_price": None,
                                                    "price": None,
                                                    "text": "Köpskydd 77 kr",
                                                },
                                            ],
                                            "sub_header": None,
                                            "sub_icon": None,
                                            "text": "Så funkar frakt med köpskydd",
                                        }
                                    ],
                                    "header": {
                                        "icon_url": None,
                                        "text": "Frakt med köpskydd",
                                    },
                                },
                                "price_points": [
                                    {
                                        "campaign_text": None,
                                        "icon_url": None,
                                        "icon_url_dark": None,
                                        "original_price": 49,
                                        "price": 49,
                                        "text": "Spårbar frakt 49 kr + köpskydd 77 kr",
                                    }
                                ],
                                "transaction_state_information": None,
                            },
                            "shipping_buy_now_entrance": {
                                "icon": {
                                    "id": "icon_shipping_buy_now_primary",
                                    "label": "Köp nu",
                                    "src_dark": "https://public-assets.blocketcdn.se/static/icons/buy-now-for-shipping/shipping_icon_primary.png",
                                    "src_light": "https://public-assets.blocketcdn.se/static/icons/buy-now-for-shipping/shipping_icon_primary.png",
                                },
                                "info_text": None,
                                "is_enabled": True,
                                "link": None,
                                "text": "Köp nu",
                                "url": "https://www.blocket.se/frakt/kop-nu-knapp?ad_id=1213640595&partner=other&source=ad&seller_blocket_account_id=2691672",
                            },
                            "state": "activated",
                            "transaction_dates": None,
                            "urls": {
                                "seller_activate": "https://www.blocket.se/frakt/saljare-aktiverar-start?ad_id=1213640595&source=ai"
                            },
                        },
                    },
                    "inventory": {
                        "context": {
                            "gam": {
                                "api_keywords": {
                                    "adid": ["1213640595"],
                                    "adtitle": [
                                        "Ralph%20Lauren%20Rock%20herrock%20h%C3%B6stjacka%20herrjacka%20Herr%20S"
                                    ],
                                    "adtype": ["s_p"],
                                    "appmode": ["notinapp"],
                                    "blocket_section": ["4000", "4080"],
                                    "companyad": ["0"],
                                    "country": ["sverige"],
                                    "country_code": ["se"],
                                    "county": ["21"],
                                    "id": ["1213640595"],
                                    "itemimage": [
                                        "https://i.blocketcdn.se/pictures/recommerce/1213640595/fe21cc7b-8613-4f7f-846a-67d86fe0dcb9.jpg"
                                    ],
                                    "itemsecuredthumb": [
                                        "https://i.blocketcdn.se/pictures/recommerce/1213640595/fe21cc7b-8613-4f7f-846a-67d86fe0dcb9.jpg"
                                    ],
                                    "itemthumb": [
                                        "https://i.blocketcdn.se/pictures/recommerce/1213640595/fe21cc7b-8613-4f7f-846a-67d86fe0dcb9.jpg"
                                    ],
                                    "lkf": ["0780"],
                                    "municipality": ["251"],
                                    "nmp_vertical": ["recommerce"],
                                    "page": ["object"],
                                    "price": ["1100"],
                                    "price_range_1": ["1001-1500"],
                                    "publisher": ["blocket"],
                                    "services": [],
                                },
                                "client_keywords": {
                                    "cmp_advertising": "cmp_advertising",
                                    "logged_in": "loggedin",
                                    "page_gen": "pagegen",
                                    "ppid_1": "schuserhash",
                                    "ppid_2": "schenvhash",
                                    "screen_height": "screenheight",
                                    "screen_width": "screenwidth",
                                    "site_mode": "sitemode",
                                    "supply_type": "supply_type",
                                    "viewport_height": "viewportheight",
                                    "viewport_width": "viewportwidth",
                                },
                                "network_id": "23166775775",
                            }
                        },
                        "placements": [
                            {
                                "gam": {
                                    "keywords": {
                                        "adformat": ["wallpaper", "toppanorama_wde"],
                                        "adsize": ["980x240", "1600x900", "2x1"],
                                    },
                                    "media_types": [
                                        {
                                            "height": 240,
                                            "type": "display",
                                            "width": 980,
                                        },
                                        {
                                            "height": 240,
                                            "type": "display",
                                            "width": 970,
                                        },
                                        {
                                            "height": 900,
                                            "type": "display",
                                            "width": 1600,
                                        },
                                        {"type": "native"},
                                    ],
                                    "path": "23166775775/blocket-recommerce/wde/object/top_1",
                                    "target_id": "placement_panorama",
                                },
                                "type": "banner",
                                "vendor": "gam",
                                "viewport": "large",
                            },
                            {
                                "gam": {
                                    "keywords": {
                                        "adformat": ["post_it_1"],
                                        "adsize": ["250x360", "250x480", "2x1"],
                                    },
                                    "media_types": [
                                        {
                                            "height": 360,
                                            "type": "display",
                                            "width": 250,
                                        },
                                        {
                                            "height": 480,
                                            "type": "display",
                                            "width": 250,
                                        },
                                        {"type": "native"},
                                    ],
                                    "path": "23166775775/blocket-recommerce/wde/object/postit_1",
                                    "target_id": "placement_widescreen-1",
                                },
                                "type": "banner",
                                "vendor": "gam",
                                "viewport": "large",
                            },
                            {
                                "gam": {
                                    "keywords": {
                                        "adformat": ["post_it_2"],
                                        "adsize": ["250x360", "250x480", "2x1"],
                                    },
                                    "media_types": [
                                        {
                                            "height": 360,
                                            "type": "display",
                                            "width": 250,
                                        },
                                        {
                                            "height": 480,
                                            "type": "display",
                                            "width": 250,
                                        },
                                        {"type": "native"},
                                    ],
                                    "path": "23166775775/blocket-recommerce/wde/object/postit_2",
                                    "target_id": "placement_widescreen-2",
                                },
                                "type": "banner",
                                "vendor": "gam",
                                "viewport": "large",
                            },
                            {
                                "gam": {
                                    "keywords": {
                                        "adformat": ["post_it_3"],
                                        "adsize": ["250x360", "250x480", "2x1"],
                                    },
                                    "media_types": [
                                        {
                                            "height": 360,
                                            "type": "display",
                                            "width": 250,
                                        },
                                        {
                                            "height": 480,
                                            "type": "display",
                                            "width": 250,
                                        },
                                        {"type": "native"},
                                    ],
                                    "path": "23166775775/blocket-recommerce/wde/object/postit_3",
                                    "target_id": "placement_widescreen-3",
                                },
                                "type": "banner",
                                "vendor": "gam",
                                "viewport": "large",
                            },
                            {
                                "gam": {
                                    "keywords": {
                                        "adformat": ["post_it_4"],
                                        "adsize": ["250x360", "250x480", "2x1"],
                                    },
                                    "media_types": [
                                        {
                                            "height": 360,
                                            "type": "display",
                                            "width": 250,
                                        },
                                        {
                                            "height": 480,
                                            "type": "display",
                                            "width": 250,
                                        },
                                        {"type": "native"},
                                    ],
                                    "path": "23166775775/blocket-recommerce/wde/object/postit_4",
                                    "target_id": "placement_widescreen-4",
                                },
                                "type": "banner",
                                "vendor": "gam",
                                "viewport": "large",
                            },
                            {
                                "gam": {
                                    "keywords": {
                                        "adformat": ["pricedisplay"],
                                        "adsize": ["185x20", "2x1", "300x20"],
                                    },
                                    "media_types": [
                                        {"height": 20, "type": "display", "width": 185},
                                        {"height": 20, "type": "display", "width": 300},
                                        {"type": "native"},
                                    ],
                                    "path": "23166775775/blocket-recommerce/wde/object/price",
                                    "target_id": "placement_price",
                                },
                                "type": "banner",
                                "vendor": "gam",
                                "viewport": "large",
                            },
                            {
                                "gam": {
                                    "keywords": {
                                        "adformat": ["infor_kopet_1"],
                                        "adsize": ["1x1"],
                                    },
                                    "media_types": [
                                        {"height": 92, "type": "display", "width": 368},
                                        {"height": 1, "type": "display", "width": 1},
                                        {"type": "native"},
                                    ],
                                    "path": "23166775775/blocket-recommerce/wph/object/native_1",
                                    "target_id": "infor_kopet_1",
                                },
                                "type": "infor_kopet",
                                "vendor": "gam",
                                "viewport": "small",
                            },
                            {
                                "gam": {
                                    "keywords": {
                                        "adformat": ["infor_kopet_2"],
                                        "adsize": ["1x1"],
                                    },
                                    "media_types": [
                                        {"height": 92, "type": "display", "width": 368},
                                        {"height": 1, "type": "display", "width": 1},
                                        {"type": "native"},
                                    ],
                                    "path": "23166775775/blocket-recommerce/wph/object/native_2",
                                    "target_id": "infor_kopet_2",
                                },
                                "type": "infor_kopet",
                                "vendor": "gam",
                                "viewport": "small",
                            },
                            {
                                "gam": {
                                    "keywords": {
                                        "adformat": ["panorama_bottom"],
                                        "adsize": ["320x320", "2x1"],
                                    },
                                    "media_types": [
                                        {
                                            "height": 320,
                                            "type": "display",
                                            "width": 320,
                                        },
                                        {"type": "native"},
                                    ],
                                    "path": "23166775775/blocket-recommerce/wph/object/bottom_1",
                                    "target_id": "vi_panorama_bottom",
                                },
                                "type": "banner",
                                "vendor": "gam",
                                "viewport": "small",
                            },
                            {
                                "gam": {
                                    "keywords": {
                                        "adformat": ["karusell"],
                                        "adsize": ["320x320", "1x1"],
                                    },
                                    "media_types": [
                                        {
                                            "height": 320,
                                            "type": "display",
                                            "width": 320,
                                        },
                                        {"type": "native"},
                                    ],
                                    "path": "23166775775/blocket-recommerce/wph/object/incarousel",
                                    "target_id": "vi_image_integration",
                                },
                                "type": "banner",
                                "vendor": "gam",
                                "viewport": "small",
                            },
                            {
                                "safe_purchase": {
                                    "body": "Var försiktig med att överföra pengar till privatpersoner. Använd istället Blocketpaketet när pengar och varor ska skickas. Med Blocketpaketet identifierar sig både köpare och säljare med BankID och betalningen går via vår betalpartner Rocker. Tryggt för båda parter!",
                                    "header": "Trygg affär",
                                    "links": [
                                        {
                                            "label": "Läs Blockets tips för en trygg affär",
                                            "type": "info",
                                            "url": "https://www.blocket.se/om/sakerhet/nar-nagot-ska-skickas",
                                        },
                                    ],
                                    "partners": [
                                        {
                                            "body": "",
                                            "header": "Trygghet & säkerhet på Blocket",
                                            "icon_png": "https://images.ctfassets.net/rvdf5xmxjruf/3HHLh42mIq5gH57G9BDrQV/6958286baedcdce18a75cc53d8e6b0c9/general_safetytip.png",
                                            "icon_svg": "https://images.ctfassets.net/rvdf5xmxjruf/4SPOb3fBJbo3QxUmfln9V3/f035d38afc67752b897b025a6e3106d7/general_safetytip.svg",
                                            "id": "safety tip",
                                            "is_advertisement": False,
                                            "link": {
                                                "label": "När något ska skickas",
                                                "url": "https://www.blocket.se/om/sakerhet/nar-nagot-ska-skickas",
                                            },
                                            "tracking_creative": "safety tip active blocketpaketet categories",
                                            "tracking_position": "safety tip",
                                        },
                                    ],
                                },
                                "type": "safe_purchase",
                                "vendor": "blocket",
                                "viewport": "universal",
                            },
                        ],
                    },
                },
            ),
        )
        assert api.get_ad_by_id(1213640595, as_objects=True) == AdByIdResults(
            data=AdByIdData(
                ad_id="1213640595",
                ad_status="active",
                advertiser=AdByIdAdvertiser(
                    account_id="2691672",
                    contact_methods=AdByIdContactMethods(mc=True),
                    name="Växjö",
                    public_profile=AdByIdPublicProfile(
                        account_created_at="2016-04-30T08:07:49.607Z",
                        badges=[
                            {
                                "description": "405 annonser inom 6 mån",
                                "icon_bui": "IconMedalMulticolor",
                                "icon_src": "https://public-assets.blocketcdn.se/static/icons/medal.png",
                                "id": "active-user",
                                "label": "Aktiv på Blocket",
                            }
                        ],
                        blocket_account_id="1223",
                        display_name="Växjö",
                        number_of_active_ads=136,
                        reviews=AdByIdReviews(
                            overall_score=97, reviews_received_count=39
                        ),
                        verified=True,
                        verified_label="BankID",
                    ),
                    type="private",
                ),
                body="A nice body!",
                category=[
                    AdByIdCategory(id="4000", name="Personligt"),
                    AdByIdCategory(id="4080", name="Kläder & skor"),
                ],
                images=[
                    AdByIdImage(
                        height=1024,
                        type="image",
                        url="https://i.blocketcdn.se/pictures/recommerce/1213640595/fe21cc7b-8613-4f7f-846a-67d86fe0dcb9.jpg",
                        width=768,
                    )
                ],
                latitude=None,
                list_id="1213640595",
                list_time="2025-09-23T18:48:34+02:00",
                location=[
                    AdByIdLocation(id="21", name="Kronoberg", query_key="r"),
                    AdByIdLocation(id="251", name="Växjö", query_key="m"),
                ],
                longitude=None,
                map=AdByIdMap(
                    image_url="https://api.hitta.se/image/v2/0/15?location=%7B%22zip%22:%2235244%22%7D&zoom.to=location",
                    label="352 44 Växjö, Kronobergs län",
                    type="zipcode",
                ),
                map_url="https://www.hitta.se/kartan/partner/blocketv2?ad_id=1213640595",
                parameter_groups=[
                    AdByIdParameterGroup(
                        label="Allmän information",
                        parameters=[
                            AdByIdParameter(
                                id="item_condition",
                                label="Skick",
                                value="Bra skick - Sparsamt använd",
                                suffix=None,
                            )
                        ],
                        type="general",
                    ),
                    AdByIdParameterGroup(
                        label="Mer om kläderna",
                        parameters=[
                            AdByIdParameter(
                                id="clothing_kind",
                                label="Typ av plagg",
                                value="Jackor & ytterplagg",
                                suffix=None,
                            )
                        ],
                        type="clothing",
                    ),
                ],
                price=AdByIdPrice(suffix="kr", value=1100),
                saved=False,
                share_url="https://www.blocket.se/annons/kronoberg/ralph_lauren_rock_herrock_hostjacka_herrjacka_herr_s/1213640595",
                state_id="830afc45-ecfa-4ce7-b400-07736a7a4fcb",
                subject="Ralph Lauren Rock herrock höstjacka herrjacka Herr S",
                type="s",
                zipcode="35244",
                blocket_package=AdByIdBlocketPackage(
                    activated_providers=[
                        {"cost": 126, "id": "d9f6c92d-0b18-4bb5-b5cf-479227a8239c"}
                    ],
                    ad_id="1213640595",
                    blocket_payment_backwards_compatability=None,
                    buyers_protection_fee=77,
                    eligible_providers=[{"id": "d9f6c92d-0b18-4bb5-b5cf-479227a8239c"}],
                    fail_code=None,
                    failure=None,
                    feature_swish=True,
                    features=AdByIdFeatures(is_part_of_merge=True),
                    is_in_dispute=False,
                    partner="other",
                    payment_methods=[
                        {
                            "id": "mastercard",
                            "label": "Mastercard",
                            "src_dark": "https://public-assets.blocketcdn.se/static/icons/payment-methods/mastercard_dark.png",
                            "src_light": "https://public-assets.blocketcdn.se/static/icons/payment-methods/mastercard.png",
                        }
                    ],
                    payment_request_entrance={
                        "icon": {
                            "id": "icon_shipping_payment_request_secondary",
                            "label": "Skicka prisförslag",
                            "src_dark": "https://public-assets.blocketcdn.se/static/icons/buy-now-for-shipping/shipping_icon_primary.png",
                            "src_light": "https://public-assets.blocketcdn.se/static/icons/buy-now-for-shipping/shipping_icon_secondary.png",
                        },
                        "info_text": None,
                        "is_enabled": True,
                        "link": None,
                        "text": "Skicka prisförslag",
                        "url": "https://www.blocket.se/frakt/kopare-knapp?ad_id=1213640595&partner=other&source=ad&seller_blocket_account_id=2691672",
                    },
                    payment_url=None,
                    service_data={
                        "information": {
                            "content": [
                                {
                                    "bullet_points": [
                                        "Godkänn varan innan säljaren får betalt",
                                        "Hjälp om varan behöver reklameras",
                                        "Klimatkompenserad frakt med förväntad leveranstid på 1-2 vardagar",
                                    ],
                                    "info_text": "Köpskyddet är baserat på varans pris.",
                                    "links": [
                                        {
                                            "text": "Så funkar frakt med köpskydd",
                                            "url": "https://www.blocket.se/om-kopskydd?hideui=1",
                                        }
                                    ],
                                    "price_points": [
                                        {
                                            "campaign_text": None,
                                            "icon_url": "https://public-assets.blocketcdn.se/static/icons/buyers-protection-fee/shipping_icon.png",
                                            "icon_url_dark": "https://public-assets.blocketcdn.se/static/icons/buyers-protection-fee/shipping_icon_dark_mode.png",
                                            "original_price": 49,
                                            "price": 49,
                                            "text": "DB Schenker 49 kr",
                                        },
                                        {
                                            "campaign_text": None,
                                            "icon_url": "https://public-assets.blocketcdn.se/static/icons/buyers-protection-fee/plus.png",
                                            "icon_url_dark": "https://public-assets.blocketcdn.se/static/icons/buyers-protection-fee/plus_dark_mode.png",
                                            "original_price": None,
                                            "price": None,
                                            "text": "Köpskydd 77 kr",
                                        },
                                    ],
                                    "sub_header": None,
                                    "sub_icon": None,
                                    "text": "Så funkar frakt med köpskydd",
                                }
                            ],
                            "header": {"icon_url": None, "text": "Frakt med köpskydd"},
                        },
                        "price_points": [
                            {
                                "campaign_text": None,
                                "icon_url": None,
                                "icon_url_dark": None,
                                "original_price": 49,
                                "price": 49,
                                "text": "Spårbar frakt 49 kr + köpskydd 77 kr",
                            }
                        ],
                        "transaction_state_information": None,
                    },
                    shipping_buy_now_entrance={
                        "icon": {
                            "id": "icon_shipping_buy_now_primary",
                            "label": "Köp nu",
                            "src_dark": "https://public-assets.blocketcdn.se/static/icons/buy-now-for-shipping/shipping_icon_primary.png",
                            "src_light": "https://public-assets.blocketcdn.se/static/icons/buy-now-for-shipping/shipping_icon_primary.png",
                        },
                        "info_text": None,
                        "is_enabled": True,
                        "link": None,
                        "text": "Köp nu",
                        "url": "https://www.blocket.se/frakt/kop-nu-knapp?ad_id=1213640595&partner=other&source=ad&seller_blocket_account_id=2691672",
                    },
                    state="activated",
                    transaction_dates=None,
                    urls=AdByIdUrls(
                        seller_activate="https://www.blocket.se/frakt/saljare-aktiverar-start?ad_id=1213640595&source=ai"
                    ),
                ),
            ),
            inventory=AdByIdInventory(
                context=AdByIdContext(
                    gam=AdByIdGamContext(
                        api_keywords=AdByIdGamApiKeywords(
                            adid=["1213640595"],
                            adtitle=[
                                "Ralph%20Lauren%20Rock%20herrock%20h%C3%B6stjacka%20herrjacka%20Herr%20S"
                            ],
                            adtype=["s_p"],
                            appmode=["notinapp"],
                            blocket_section=["4000", "4080"],
                            companyad=["0"],
                            country=["sverige"],
                            country_code=["se"],
                            county=["21"],
                            id=["1213640595"],
                            itemimage=[
                                "https://i.blocketcdn.se/pictures/recommerce/1213640595/fe21cc7b-8613-4f7f-846a-67d86fe0dcb9.jpg"
                            ],
                            itemsecuredthumb=[
                                "https://i.blocketcdn.se/pictures/recommerce/1213640595/fe21cc7b-8613-4f7f-846a-67d86fe0dcb9.jpg"
                            ],
                            itemthumb=[
                                "https://i.blocketcdn.se/pictures/recommerce/1213640595/fe21cc7b-8613-4f7f-846a-67d86fe0dcb9.jpg"
                            ],
                            livingarea=None,
                            lkf=["0780"],
                            municipality=["251"],
                            nmp_vertical=["recommerce"],
                            page=["object"],
                            price=["1100"],
                            price_range_2=None,
                            publisher=["blocket"],
                            services=[],
                        ),
                        client_keywords=AdByIdClientKeywords(
                            cmp_advertising="cmp_advertising",
                            logged_in="loggedin",
                            page_gen="pagegen",
                            ppid_1="schuserhash",
                            ppid_2="schenvhash",
                            screen_height="screenheight",
                            screen_width="screenwidth",
                            site_mode="sitemode",
                            supply_type="supply_type",
                            viewport_height="viewportheight",
                            viewport_width="viewportwidth",
                        ),
                    ),
                    network_id=None,
                )
            ),
            placements=None,
        )


class Test_GetUserById:
    @respx.mock
    def test_get_user_by_id(self) -> None:
        respx.get(f"{BASE_URL}/profile-be/v1/public-profiles/1234").mock(
            return_value=Response(
                status_code=200,
                json={
                    "account": {"account_id": 1234, "name": "Janne"},
                },
            ),
        )
        assert api.get_user_by_id(1234) == {
            "account": {"account_id": 1234, "name": "Janne"}
        }

    @respx.mock
    def test_get_user_by_id_as_objects(self) -> None:
        respx.get(f"{BASE_URL}/profile-be/v1/public-profiles/1234").mock(
            return_value=Response(
                status_code=200,
                json={
                    "account": {
                        "blocket_account_id": "1234",
                        "created_at": "2020-10-10T15:45:06.407660",
                        "is_verified": True,
                        "name": "Janne",
                        "on_blocket_since": "På Blocket sedan 2020",
                        "verified_with": "Verifierad",
                    },
                    "active_ads": {
                        "ads": [
                            {
                                "ad_id": "111",
                                "ad_url": "https://blocket.se/annons/111",
                                "image_url": "https://i.blocketcdn.se/pictures/recommerce/111/3906d5f8-624e-4738-965d-d57040c5710d.jpg",
                                "price": "18 000 kr",
                                "region": "Stockholms stad - Östermalm, Djurgården",
                                "subject": "B&O Musikanläggning",
                            },
                        ],
                        "label_primary": "Aktiva annonser",
                        "label_secondary": "(1)",
                    },
                    "badges": [
                        {
                            "description": "8 annonser inom 6 mån",
                            "icon": "https://public-assets.blocketcdn.se/static/icons/medal.png",
                            "icon_blocket_ui": "IconMedalMulticolor",
                            "id": "active-user",
                            "label": "Aktiv på Blocket",
                        },
                    ],
                    "co2_savings": {
                        "date_range": "1 apr - idag",
                        "equivalent": "Det motsvarar produktionen av ungefär 7 cyklar.",
                        "text": "Har sparat 696 kg CO₂e.",
                    },
                    "profile_info": {
                        "description": None,
                        "has_reviews": False,
                        "name": "Janne",
                    },
                    "review_scores": None,
                },
            ),
        )
        assert api.get_user_by_id(1234, as_objects=True) == BlocketUser(
            account=BlocketUserAccount(
                blocket_account_id="1234",
                created_at=datetime.datetime(2020, 10, 10, 15, 45, 6, 407660),
                is_verified=True,
                name="Janne",
                on_blocket_since="På Blocket sedan 2020",
                verified_with="Verifierad",
            ),
            active_ads=BlocketUserActiveAds(
                ads=[
                    BlocketUserAd(
                        ad_id="111",
                        ad_url="https://blocket.se/annons/111",
                        image_url="https://i.blocketcdn.se/pictures/recommerce/111/3906d5f8-624e-4738-965d-d57040c5710d.jpg",
                        price="18 000 kr",
                        region="Stockholms stad - Östermalm, Djurgården",
                        subject="B&O Musikanläggning",
                    )
                ],
                label_primary="Aktiva annonser",
                label_secondary="(1)",
            ),
            badges=[
                BlocketUserBadge(
                    description="8 annonser inom 6 mån",
                    icon="https://public-assets.blocketcdn.se/static/icons/medal.png",
                    icon_blocket_ui="IconMedalMulticolor",
                    id="active-user",
                    label="Aktiv på Blocket",
                )
            ],
            co2_savings=BlocketUserCO2Savings(
                date_range="1 apr - idag",
                equivalent="Det motsvarar produktionen av ungefär 7 cyklar.",
                text="Har sparat 696 kg CO₂e.",
            ),
            profile_info=BlocketUserProfileInfo(
                description=None, has_reviews=False, name="Janne"
            ),
            review_scores=None,
        )


class Test_SavedAds:
    @respx.mock
    def test_save_ad(self) -> None:
        respx.put(f"{BASE_URL}/search_bff/v1/saved_content/1234").mock(
            return_value=Response(
                status_code=204,
            ),
        )
        assert api.save_ad(1234) == {"status_code": 204}

    @respx.mock
    def test_get_saved_ads(self) -> None:
        respx.get(f"{BASE_URL}/search_bff/v1/saved_content?lim=100").mock(
            return_value=Response(
                status_code=200,
                json={
                    "data": [
                        {"id": "1", "name": "Nice jeans"},
                        {"id": "2", "name": "A very fast bike"},
                    ],
                },
            ),
        )
        assert api.get_saved_ads() == {
            "data": [
                {"id": "1", "name": "Nice jeans"},
                {"id": "2", "name": "A very fast bike"},
            ],
        }
