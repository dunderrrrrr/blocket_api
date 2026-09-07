import htpy as h
from markupsafe import Markup

from docs.components import index as c
from docs.components_base import fragment, page


def content() -> list[h.Node]:
    return [
        c.hero(),
        c.examples_section(),
        c.features(),
        c.uv_section(),
        c.cta(),
    ]


def view() -> Markup:
    return page(
        active="index",
        title="BlocketAPI — The unofficial API for blocket.se",
        description="BlocketAPI is the leading developer API for blocket.se. Search ads, cars, boats, motorcycles and more. Free to use, no API key required.",
        content_fn=content,
    )


def fragment_view() -> str:
    return fragment(content)
