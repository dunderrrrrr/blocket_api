import pytest
from blocket_api.blocket import BlocketAPI, LimitError

api = BlocketAPI("token")


def test_limit_errors():
    with pytest.raises(LimitError):
        api.get_listings(limit=100)

    with pytest.raises(LimitError):
        api.custom_search("saab", limit=100)


def test_typeerrors():
    with pytest.raises(TypeError):
        api.custom_search()  # missing search query

    with pytest.raises(TypeError):
        BlocketAPI()
