import htpy as h

from docs.components import quickstart as c
from markupsafe import Markup
from docs.components_base import doc_layout, fragment, page, page_hero


def content() -> list[h.Node]:
    return [
        page_hero(
            "Quickstart",
            "Get from zero to your first API response in under 5 minutes — no account, no API key.",
            "Quickstart",
        ),
        h.section(".section")[
            h.div(".container")[
                doc_layout(
                    c.sidebar(),
                    [
                        *c.installation(),
                        *c.first_search(),
                        *c.uv_section(),
                    ],
                ),
            ],
        ],
    ]


def view() -> Markup:
    return page(
        active="quickstart",
        title="Quickstart — BlocketAPI",
        description="Install BlocketAPI and make your first search in under 5 minutes. Supports Python, REST, curl and JavaScript.",
        content_fn=content,
    )


def fragment_view() -> str:
    return fragment(content)
