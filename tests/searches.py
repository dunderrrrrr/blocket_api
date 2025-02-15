import respx
from httpx import Response
from blocket_api.blocket import BASE_URL, BlocketAPI, Region

api = BlocketAPI("token")


@respx.mock
def test_saved_searches():
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
def test_for_search_id():
    respx.get(f"{BASE_URL}/saved/v2/searches_content/123?lim=99").mock(
        return_value=Response(status_code=200, json={"data": "listings-data"}),
    )
    assert api.get_listings(search_id=123) == {"data": "listings-data"}


@respx.mock
def test_for_search_id_mobility():
    respx.get(f"{BASE_URL}/saved/v2/searches_content/123?lim=99").mock(
        return_value=Response(status_code=404),
    )
    respx.get(f"{BASE_URL}/mobility-saved-searches/v1/searches/123/ads?lim=99").mock(
        return_value=Response(status_code=200, json={"data": "mobility-data"}),
    )
    assert api.get_listings(search_id=123) == {"data": "mobility-data"}


@respx.mock
def test_custom_search():
    respx.get(
        f"{BASE_URL}/search_bff/v2/content?lim=99&q=saab&r=20&status=active"
    ).mock(
        return_value=Response(status_code=200, json={"data": {"location": "halland"}}),
    )
    assert api.custom_search("saab", Region.halland) == {
        "data": {"location": "halland"}
    }
