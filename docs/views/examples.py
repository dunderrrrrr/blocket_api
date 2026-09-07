import htpy as h
from markupsafe import Markup

from docs.components import examples as c
from docs.components_base import (
    GITHUB,
    fragment,
    page,
    page_hero,
    section_header,
    tip_box,
)


def content() -> list[h.Node]:
    return [
        page_hero(
            "Examples",
            "Ready-to-run code snippets covering the most common use cases. Copy, paste, run.",
            "Examples",
        ),
        h.section(".section")[
            h.div(".container")[
                section_header(
                    "Code Examples",
                    "From simple searches to production scripts",
                    "Every example runs standalone with uv — no environment setup required.",
                ),
                h.div(".example-cards")[c.cards()],
                tip_box(
                    "🤝",
                    [
                        "Have an example you'd like to share? ",
                        h.a(".link", href=GITHUB + "/issues", target="_blank")[
                            "Open an issue on GitHub ↗"
                        ],
                        " or submit a PR.",
                    ],
                    kind="tip",
                ),
            ],
        ],
    ]


def view() -> Markup:
    return page(
        active="examples",
        title="Examples — BlocketAPI",
        description="Ready-to-run BlocketAPI code examples: general search, car filters, price alerts, CSV export, pagination, and more.",
        content_fn=content,
    )


def fragment_view() -> str:
    return fragment(content)
