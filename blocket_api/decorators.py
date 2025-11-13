from collections.abc import Callable
from functools import wraps
from typing import Any

import httpx

from .constants import SITE_URL


class TokenError(Exception): ...


def auth_token(method: Callable) -> Callable:
    @wraps(method)
    def wrapper(self: Any, *args: Any, **kwargs: Any) -> Callable:
        if not self.token:
            raise TokenError("Token is required, see documentation.")
        return method(self, *args, **kwargs)

    return wrapper


def public_token(method: Callable) -> Callable:
    @wraps(method)
    def wrapper(self: Any, *args: Any, **kwargs: Any) -> Callable:
        if not self.token:
            response = httpx.get(
                f"{SITE_URL}/api/adout-api-route/refresh-token-and-validate-session"
            )
            response.raise_for_status()
            self.token = response.json()["bearerToken"]
        return method(self, *args, **kwargs)

    return wrapper
