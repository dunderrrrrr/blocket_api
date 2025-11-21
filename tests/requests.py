import httpx
import respx

from blocket_api import (
    BlocketAPI,
    BoatType,
    CarAd,
    CarModel,
    CarSortOrder,
    CarTransmission,
    Category,
    Location,
    RecommerceAd,
    SortOrder,
    SubCategory,
)
from blocket_api.constants import SITE_URL

api = BlocketAPI()


class Test_Search:
    @respx.mock
    def test_search(self) -> None:
        expected_url = (
            f"{SITE_URL}/recommerce-search-page/api/search/SEARCH_ID_BAP_COMMON"
            "?q=audi+q5"
            "&sort=RELEVANCE"
        )
        respx.get(expected_url).mock(
            return_value=httpx.Response(200, json={"status": "ok"})
        )
        result = api.search("audi q5")
        assert result == {"status": "ok"}

    @respx.mock
    def test_search_sortorder_published_desc(self) -> None:
        expected_url = (
            f"{SITE_URL}/recommerce-search-page/api/search/SEARCH_ID_BAP_COMMON"
            "?q=audi+q5"
            "&sort=PUBLISHED_DESC"
        )
        respx.get(expected_url).mock(
            return_value=httpx.Response(200, json={"status": "ok"})
        )
        result = api.search("audi q5", sort_order=SortOrder.PUBLISHED_DESC)
        assert result == {"status": "ok"}

    @respx.mock
    def test_search_location(self) -> None:
        expected_url = (
            f"{SITE_URL}/recommerce-search-page/api/search/SEARCH_ID_BAP_COMMON"
            "?q=audi+q5"
            "&sort=PUBLISHED_DESC"
            "&location=0.300003"
            "&location=0.300001"
        )
        respx.get(expected_url).mock(
            return_value=httpx.Response(200, json={"status": "ok"})
        )
        result = api.search(
            "audi q5",
            sort_order=SortOrder.PUBLISHED_DESC,
            locations=[
                Location.UPPSALA,
                Location.STOCKHOLM,
            ],
        )
        assert result == {"status": "ok"}

    @respx.mock
    def test_search_category(self) -> None:
        expected_url = (
            f"{SITE_URL}/recommerce-search-page/api/search/SEARCH_ID_BAP_COMMON"
            "?q=audi+q5"
            "&sort=PUBLISHED_DESC"
            "&category=0.90"
        )
        respx.get(expected_url).mock(
            return_value=httpx.Response(200, json={"status": "ok"})
        )
        result = api.search(
            "audi q5",
            sort_order=SortOrder.PUBLISHED_DESC,
            category=Category.FORDONSTILLBEHOR,
        )
        assert result == {"status": "ok"}

    @respx.mock
    def test_sub_category(self) -> None:
        expected_url = (
            f"{SITE_URL}/recommerce-search-page/api/search/SEARCH_ID_BAP_COMMON"
            "?q=hammare"
            "&sort=RELEVANCE"
            "&sub_category=1.67.5219"
        )
        respx.get(expected_url).mock(
            return_value=httpx.Response(200, json={"status": "ok"})
        )
        result = api.search(
            "hammare",
            sub_category=SubCategory.VERKTYG,
        )
        assert result == {"status": "ok"}


class Test_SearchCar:
    @respx.mock
    def test_search_car(self) -> None:
        expected_url = (
            f"{SITE_URL}/mobility/search/api/search/SEARCH_ID_CAR_USED"
            "?sort=MILEAGE_ASC"
            "&make=0.744"
            "&price_from=1000"
            "&price_to=50000"
            "&transmission=2"
        )
        respx.get(expected_url).mock(
            return_value=httpx.Response(200, json={"status": "ok"})
        )
        result = api.search_car(
            sort_order=CarSortOrder.MILEAGE_ASC,
            models=[CarModel.AUDI],
            price_from=1000,
            price_to=50000,
            transmissions=[CarTransmission.AUTOMATIC],
        )
        assert result == {"status": "ok"}


class Test_SearchBoat:
    @respx.mock
    def test_search_boat(self) -> None:
        expected_url = (
            f"{SITE_URL}/mobility/search/api/search/SEARCH_ID_BOAT_USED"
            "?q=Mercury"
            "&sort=RELEVANCE"
            "&class=2184"
            "&location=0.300001"
            "&price_from=20000"
            "&price_to=90000"
            "&length_feet_from=10"
            "&length_feet_to=15"
        )
        respx.get(expected_url).mock(
            return_value=httpx.Response(200, json={"status": "ok"})
        )
        result = api.search_boat(
            "Mercury",
            types=[BoatType.DAYCRUISER],
            locations=[Location.STOCKHOLM],
            length_from=10,
            length_to=15,
            price_from=20000,
            price_to=90000,
        )
        assert result == {"status": "ok"}


class Test_GetAd:
    @respx.mock
    def test_get_ad_recommerce(self) -> None:
        expected_url = f"{SITE_URL}/recommerce/forsale/item/12345567"
        respx.get(expected_url).mock(
            return_value=httpx.Response(
                200,
                content=b'<script>window.__staticRouterHydrationData = JSON.parse("{"some": "json here"}");</script>',
            )
        )
        result = api.get_ad(RecommerceAd(12345567))
        assert result == {"some": "json here"}

    @respx.mock
    def test_get_ad_car(self) -> None:
        expected_url = f"{SITE_URL}/mobility/item/123456"
        html = """
            <div class="grid grid-cols-1 md:grid-cols-3 md:gap-x-32">

                <h1 class="t1">Volvo V60</h1>
                <p class="s-text-subtle mt-8">D4 AWD Momentum</p>

                <div class="grid gap-24">
                    <div class="flex gap-16 hyphens-auto">
                        <span class="s-text-subtle">Modellår</span>
                        <p class="m-0 font-bold">2020</p>
                    </div>
                    <div class="flex gap-16 hyphens-auto">
                        <span class="s-text-subtle">Miltal</span>
                        <p class="m-0 font-bold">4500</p>
                    </div>
                </div>

                <div class="border-t pt-40 mt-40">
                    <p class="s-text-subtle mb-0">Pris</p>
                    <span class="t2">389 000 kr</span>
                </div>

                <section class="border-t mt-40 pt-40">
                    <h2 class="t3 mb-0">Beskrivning</h2>
                    <div class="whitespace-pre-wrap">Mycket fin bil i nyskick.</div>
                </section>

                <section class="border-t pt-40 mt-40">
                    <h2 class="t3 mb-0">Utrustning</h2>
                    <ul>
                        <li>ACC Klimatanläggning</li>
                        <li>Adaptiv farthållare</li>
                    </ul>
                </section>

            </div>

            <div class="dealer">Återförsäljare</div>

            <div class="text-m flex md:flex-row flex-col md:gap-x-56 gap-y-16">
                <p class="s-text-subtle mb-0">Annons-ID</p>
                <p>123456</p>
            </div>
        """
        respx.get(expected_url).mock(
            return_value=httpx.Response(200, content=html.encode("utf-8"))
        )
        result = api.get_ad(CarAd(123456))
        assert result == {
            "url": "https://www.blocket.se/mobility/item/123456",
            "title": "Volvo V60",
            "subtitle": "D4 AWD Momentum",
            "model_year": "2020",
            "mileage": "4500",
            "price": "389 000 kr",
            "description": "Mycket fin bil i nyskick.",
            "equipment": ["ACC Klimatanläggning", "Adaptiv farthållare"],
            "seller_type": "dealer",
            "ad_id": "123456",
        }
