import httpx
import respx

from blocket_api import BlocketAPI, Category, Location, SortOrder, SubCategory
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
