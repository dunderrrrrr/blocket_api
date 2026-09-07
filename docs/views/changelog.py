import htpy as h
from flask import url_for
from markupsafe import Markup

from docs.components_base import fragment, page, page_hero


def content() -> list[h.Node]:
    return [
        page_hero(
            "Changelog",
            "Merged pull requests from GitHub — features, fixes, and improvements.",
            "Changelog",
        ),
        h.section(".section")[
            h.div(".container.container-narrow")[
                h.div(
                    "#cl-root",
                    hx_get=url_for("changelog_body"),
                    hx_trigger="load",
                    hx_swap="innerHTML",
                )[
                    h.div(".ep-spinner")[
                        h.div(".ep-spinner-ring"),
                        h.span["Loading changelog…"],
                    ],
                ],
            ],
        ],
    ]


def view() -> Markup:
    return page(
        active="changelog",
        title="Changelog — BlocketAPI",
        description="Full release history for BlocketAPI — Python library and REST API. Features, fixes and new endpoints.",
        content_fn=content,
    )


def fragment_view() -> str:
    return fragment(content)
