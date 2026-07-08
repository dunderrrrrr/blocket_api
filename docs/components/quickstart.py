import htpy as h
from flask import url_for

from docs.components_base import (
    API_BASE,
    GITHUB,
    PYPI,
    SWAGGER,
    _htmx,
    code_block,
    code_tabs,
    ic,
    sidebar_link,
    sidebar_section,
    tip_box,
)


def tab_btn(key: str, label: str, active: bool = False) -> h.Node:
    return h.button(
        ".tab-btn.active" if active else ".tab-btn",
        onclick=f"switchTab(this,'{key}')",
    )[label]


def tab_panel(key: str, content: h.Node, active: bool = False) -> h.Node:
    return h.div(".tab-panel.active" if active else ".tab-panel", id=key)[content]


# ── Code snippets ─────────────────────────────────────────────────────────────


def install_uv() -> h.Node:
    return code_block(
        "terminal",
        "SH",
        """\
# install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# add blocket-api to your project
uv add blocket-api""",
    )


def install_pip() -> h.Node:
    return code_block("terminal", "SH", "pip install blocket-api")


def first_search_py() -> h.Node:
    return code_block(
        "hello_blocket.py",
        "PY",
        """\
from blocket_api import BlocketAPI

api = BlocketAPI()
results = api.search("iPhone 15")

for item in results["docs"]:
    print(item["heading"], "-", item["price"]["amount"], "SEK")""",
    )


def first_search_rest() -> h.Node:
    return code_block(
        "terminal",
        "SH",
        f"""\
# GET {API_BASE}/v1/search
curl "{API_BASE}/v1/search?query=iPhone+15" | python3 -m json.tool""",
    )


def first_search_js() -> h.Node:
    return code_block(
        "search.js",
        "JS",
        f"""\
const res = await fetch(
  "{API_BASE}/v1/search?query=iPhone+15"
).then(r => r.json());

res.docs.forEach(item => {{
  console.log(item.heading, item.price?.amount);
}});""",
    )


def car_search() -> h.Node:
    return code_block(
        "car_search.py",
        "PY",
        """\
from blocket_api import (
    BlocketAPI, CarModel, Location, CarSortOrder,
)

api = BlocketAPI()
cars = api.search_car(
    models=[CarModel.BMW],
    locations=[Location.STOCKHOLM],
    sort_order=CarSortOrder.PRICE_ASC,
    price_to=150000,
)

for car in cars["docs"]:
    print(car["heading"], car["price"]["amount"])""",
    )


def uv_script() -> h.Node:
    return code_block(
        "my_search.py",
        "PY",
        """\
# /// script
# requires-python = ">=3.10"
# dependencies = ["blocket-api"]
# ///

from blocket_api import BlocketAPI

api = BlocketAPI()
results = api.search("Lego Technic")
print(results["docs"][0])""",
    )


def uv_run() -> h.Node:
    return code_block("terminal", "SH", "uv run my_search.py")


# ── Sidebar ───────────────────────────────────────────────────────────────────


def sidebar() -> list[h.Node]:
    return [
        sidebar_section(
            "Getting started",
            [
                sidebar_link("Installation", "#installation", active=True),
                sidebar_link("Your first search", "#first-search"),
                sidebar_link("Run with uv", "#uv"),
            ],
        ),
        sidebar_section(
            "Reference",
            [
                sidebar_link("All endpoints", url_for("endpoints")),
                sidebar_link("Swagger docs", SWAGGER),
                sidebar_link("PyPI", PYPI),
                sidebar_link("GitHub", GITHUB),
            ],
        ),
    ]


# ── Page sections ─────────────────────────────────────────────────────────────


def installation() -> list[h.Node]:
    return [
        h.h2(id="installation")["Installation"],
        h.p["BlocketAPI is available as a Python library or via direct REST calls."],
        h.div(".tab-group")[
            tab_btn("qs-uv", "uv", active=True),
            tab_btn("qs-pip", "pip"),
            tab_btn("qs-rest", "cURL"),
            tab_btn("qs-js", "js"),
        ],
        tab_panel("qs-uv", install_uv(), active=True),
        tab_panel("qs-pip", install_pip()),
        tab_panel(
            "qs-rest",
            h.p(".tab-note")[
                "No install needed. The REST API is publicly accessible at ",
                h.a(".link", href=f"{API_BASE}/v1/", target="_blank")[
                    f"{API_BASE}/v1/ ↗"
                ],
                ". See all available endpoints in the ",
                h.a(".link", href=url_for("endpoints"), **_htmx("endpoints"))[
                    "Endpoints reference"
                ],
                ".",
            ],
        ),
        tab_panel(
            "qs-js",
            h.p(".tab-note")[
                "Use any HTTP client. The examples below use the browser's native ",
                ic("fetch"),
                " API.",
            ],
        ),
        tip_box(
            "✅",
            [
                h.strong["No API key required."],
                " BlocketAPI is free and open source. ",
                h.a(".link", href=GITHUB, target="_blank")["View on GitHub ↗"],
            ],
            kind="tip",
        ),
    ]


def first_search() -> list[h.Node]:
    return [
        h.h2(".section-h2", id="first-search")["Your first search"],
        h.p[
            "Pick your language and run — responses always return a JSON object with a ",
            ic("docs"),
            " list.",
        ],
        code_tabs(
            ("Python", first_search_py()),
            ("cURL", first_search_rest()),
            ("js", first_search_js()),
        ),
        h.h3["Response shape"],
        h.p["Every endpoint returns a consistent structure:"],
        h.div(".endpoint-table")[
            h.table[
                h.thead[h.tr[h.th["Field"], h.th["Type"], h.th["Description"]]],
                h.tbody[
                    h.tr[
                        h.td[ic("docs")], h.td["list"], h.td["Array of listing objects"]
                    ],
                    h.tr[
                        h.td[ic("total")],
                        h.td["int"],
                        h.td["Total number of matching listings"],
                    ],
                    h.tr[h.td[ic("query")], h.td["str"], h.td["Echoed search query"]],
                    h.tr[
                        h.td[ic("location")],
                        h.td["str"],
                        h.td["Echoed location filter"],
                    ],
                ],
            ]
        ],
    ]


def car_search_curl() -> h.Node:
    return code_block(
        "terminal",
        "SH",
        f'curl "{API_BASE}/v1/search/car?models=BMW&locations=STOCKHOLM&sort_order=PRICE_ASC&price_to=150000"',
    )


def car_section() -> list[h.Node]:
    return [
        h.h2(".section-h2", id="car-search")["Car search"],
        h.p[
            "The ",
            ic("search_car()"),
            " method exposes rich vehicle-specific filters unavailable in a general search.",
        ],
        code_tabs(("Python", car_search()), ("cURL", car_search_curl())),
        h.p(".ref-link")[
            "See all car parameters in the ",
            h.a(
                ".link", href=url_for("endpoints") + "#search-car", **_htmx("endpoints")
            )["Endpoints reference"],
            ".",
        ],
        tip_box(
            "💡",
            [
                "Use the ",
                ic("Location"),
                " enum for consistent county names: ",
                ic("Location.STOCKHOLM"),
                ", ",
                ic("Location.GOTHENBURG"),
                ", ",
                ic("Location.MALMO"),
                ", etc.",
            ],
        ),
    ]


def uv_section() -> list[h.Node]:
    return [
        h.h2(".section-h2", id="uv")["Run scripts with uv"],
        h.p[
            "Add a ",
            ic("# /// script"),
            " block to make your script self-contained — uv reads it and installs deps automatically.",
        ],
        uv_script(),
        uv_run(),
        h.div(".btn-row")[
            h.a(".btn.btn-primary", href=url_for("endpoints"), **_htmx("endpoints"))[
                "Endpoint reference →"
            ],
            h.a(".btn.btn-secondary", href=SWAGGER, target="_blank")["Swagger ↗"],
            h.a(".btn.btn-secondary", href=GITHUB, target="_blank")["GitHub ↗"],
        ],
    ]
