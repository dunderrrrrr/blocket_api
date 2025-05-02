import pytest
from blocket_api.blocket import BlocketAPI, LimitError

api = BlocketAPI("token")


def test_limit_errors() -> None:
    with pytest.raises(LimitError):
        api.get_listings(limit=100)

    with pytest.raises(LimitError):
        api.custom_search("saab", limit=100)


def test_typeerrors() -> None:
    with pytest.raises(TypeError):
        # missing search query
        api.custom_search()  # type: ignore[call-arg]

    with pytest.raises(TypeError):
        # missing token
        BlocketAPI()  # type: ignore[call-arg]
