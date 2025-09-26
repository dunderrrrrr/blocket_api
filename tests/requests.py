import httpx
import pytest
import respx

from blocket_api.blocket import BASE_URL, APIError, BlocketAPI, _make_request

api = BlocketAPI("token")


def test_make_request_no_raise() -> None:
    _make_request(url=f"{BASE_URL}/not_found", token="token", raise_for_status=False)


@respx.mock
def test_make_request_raise_404() -> None:
    respx.get(f"{BASE_URL}/not_found").mock(
        return_value=httpx.Response(status_code=404),
    )
    with pytest.raises(APIError):
        _make_request(url=f"{BASE_URL}/not_found", token="token", raise_for_status=True)


@respx.mock
def test_make_request_raise_401() -> None:
    respx.get(f"{BASE_URL}/unauthorized").mock(
        return_value=httpx.Response(status_code=401),
    )
    with pytest.raises(APIError):
        _make_request(url=f"{BASE_URL}/unauthorized", token="token")


@respx.mock
def test_make_request_get() -> None:
    """Test make_request with GET method."""
    respx.get(BASE_URL).mock(return_value=httpx.Response(200, json={"success": True}))

    result = _make_request(url=BASE_URL, token="token")

    assert result.status_code == 200
    assert result.json() == {"success": True}


@respx.mock
def test_make_request_put() -> None:
    """Test make_request with PUT method."""
    respx.put(BASE_URL).mock(return_value=httpx.Response(200, json={"success": True}))

    result = _make_request(method=httpx.put, url=BASE_URL, token="token")

    assert result.status_code == 200
    assert result.json() == {"success": True}
