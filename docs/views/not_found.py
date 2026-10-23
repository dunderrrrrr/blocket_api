import htpy as h
from markupsafe import Markup

from docs.components_base import page, page_hero


def content() -> list[h.Node]:
    return [
        page_hero(
            "Page not found",
            "The page you're looking for doesn't exist or has been moved.",
            "404",
        ),
    ]


def view(_error: Exception) -> tuple[Markup, int]:
    return page(
        active="",
        title="Page not found — BlocketAPI",
        description="This page doesn't exist.",
        content_fn=content,
    ), 404
