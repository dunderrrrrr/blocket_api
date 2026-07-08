import htpy as h

from docs.components import python_lib as c
from docs.components_base import doc_layout, fragment, page, page_hero


def content():
    return [
        page_hero(
            "Python Library",
            "Use BlocketAPI as a Python package — typed enums, clean return values, no boilerplate.",
            "Python",
        ),
        h.section(".section")[
            h.div(".container")[
                doc_layout(
                    c.sidebar(),
                    [
                        *c.install_section(),
                        *c.methods_section(),
                    ],
                ),
            ],
        ],
    ]


def view():
    return page(
        active="python",
        title="Python Library — BlocketAPI",
        description="BlocketAPI Python package documentation — search, car, boat, motorcycle and ad detail methods.",
        content_fn=content,
    )


def fragment_view():
    return fragment(content)
