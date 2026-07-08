import htpy as h

from docs.components import tips as c
from markupsafe import Markup
from docs.components_base import doc_layout, fragment, page, page_hero


def content() -> list[h.Node]:
    return [
        page_hero(
            "Tips & Tricks",
            "Patterns and techniques to get the most out of BlocketAPI — from automation to market analysis.",
            "Tips & Tricks",
        ),
        h.section(".section")[
            h.div(".container")[
                doc_layout(
                    c.sidebar(),
                    [
                        *c.uv_tip(),
                        *c.cron_tip(),
                        *c.pagination_tip(),
                        *c.sorting_tip(),
                        *c.location_tip(),
                        *c.orgid_tip(),
                        *c.analysis_tip(),
                    ],
                ),
            ],
        ],
    ]


def view() -> Markup:
    return page(
        active="tips",
        title="Tips & Tricks — BlocketAPI",
        description="BlocketAPI tips: running scripts with uv, scheduling with cron, pagination, multi-location searches, price analysis and more.",
        content_fn=content,
    )


def fragment_view() -> str:
    return fragment(content)
