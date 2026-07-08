import htpy as h
from flask import url_for

from docs.components_base import fragment, page, page_hero


def content():
    return [
        page_hero(
            "Endpoint Reference",
            "Full parameter documentation for every BlocketAPI endpoint. All endpoints return JSON.",
            "Endpoints",
        ),
        h.section(".section")[
            h.div(".container")[
                h.div(
                    "#ep-root",
                    hx_get=url_for("endpoints_body"),
                    hx_trigger="load",
                    hx_swap="innerHTML",
                )[
                    h.div(".ep-spinner")[
                        h.div(".ep-spinner-ring"),
                        h.span["Loading API spec…"],
                    ],
                ],
            ],
        ],
    ]


def view():
    return page(
        active="endpoints",
        title="Endpoints — BlocketAPI",
        description="Full parameter reference for all BlocketAPI REST endpoints: search, car, motorcycle, boat, and ad detail.",
        content_fn=content,
    )


def fragment_view():
    return fragment(content)
