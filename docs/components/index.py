import htpy as h
from flask import url_for

from docs.components_base import (
    API_BASE,
    GITHUB,
    SWAGGER,
    _htmx,
    code_block,
    code_tabs,
    ic,
)


def pill(text: str) -> h.Node:
    return h.span(".pill")[h.span(".dot"), text]


def install_body(id_: str, cmd_id: str, cmd: str, active: bool = False) -> h.Node:
    return h.div(
        ".install-body.active" if active else ".install-body",
        id=id_,
    )[
        h.div(".install-cmd")[
            h.span(".install-prompt")["$"],
            h.code(id=cmd_id)[cmd],
            h.button(".copy-btn", onclick=f"copyCmd('{cmd_id}',this)")["Copy"],
        ],
    ]


def install_block() -> h.Node:
    return h.div(".install-block")[
        h.div(".install-tabs")[
            h.button(".install-tab.active", onclick="switchInstall(this,'uv')")["uv"],
            h.button(".install-tab", onclick="switchInstall(this,'pip')")["pip"],
            h.button(".install-tab", onclick="switchInstall(this,'curl')")["cURL"],
        ],
        install_body(
            "inst-uv",
            "cmd-uv",
            "uv add blocket-api",
            active=True,
        ),
        install_body("inst-pip", "cmd-pip", "pip install blocket-api"),
        install_body(
            "inst-curl",
            "cmd-curl",
            f'curl "{API_BASE}/v1/search?query=iPhone"',
        ),
    ]


# ── Code snippets ─────────────────────────────────────────────────────────────


def hero_code() -> h.Node:
    return code_block(
        "search.py",
        "PY",
        """\
from blocket_api import BlocketAPI

api = BlocketAPI()
results = api.search("iPhone 15")

for item in results["docs"]:
    print(
        item["heading"],
        item["price"]["amount"],
        item["location"]["name"],
    )""",
    )


def hero_response() -> h.Node:
    return code_block(
        "output",
        "JSON",
        """\
{
  "docs": [
    {
      "heading": "iPhone 15 Pro 256GB",
      "price": {"amount": 8500},
      "location": {"name": "Stockholm"}
    }
  ]
}""",
    )


def car_code() -> h.Node:
    return code_block(
        "cars.py",
        "PY",
        """\
from blocket_api import (
    BlocketAPI, CarModel,
    CarSortOrder, Location,
)

cars = BlocketAPI().search_car(
    models=[CarModel.VOLVO],
    locations=[Location.STOCKHOLM],
    sort_order=CarSortOrder.PRICE_ASC,
    price_to=80000,
    year_from=2018,
)""",
    )


def alert_code() -> h.Node:
    return code_block(
        "alert.py",
        "PY",
        f"""\
# /// script
# dependencies = ["httpx"]
# ///

import httpx, json
from pathlib import Path

SEEN = Path("seen.json")
seen = set(json.loads(SEEN.read_text()) if SEEN.exists() else [])

docs = httpx.get(
    "{API_BASE}/v1/search",
    params={{"query": "Sony WH-1000XM5", "sort_order": "PRICE_ASC"}},
).json()["docs"]

for d in docs:
    if d["price"]["amount"] <= 1800 and d["id"] not in seen:
        print(f\"🔔 {{d['heading']}} — {{d['price']['amount']}} SEK\")
        seen.add(d["id"])

SEEN.write_text(json.dumps(list(seen)))""",
    )


def uv_inline_code() -> h.Node:
    return code_block(
        "blocket.py",
        "PY",
        """\
# /// script
# requires-python = ">=3.10"
# dependencies = ["blocket-api"]
# ///

from blocket_api import BlocketAPI

api = BlocketAPI()
results = api.search("Lego Technic")
print(results["docs"][:5])""",
    )


def uv_run_code() -> h.Node:
    return code_block("terminal", "SH", "uv run blocket.py")


# ── Page sections ─────────────────────────────────────────────────────────────


def hero() -> h.Node:
    return h.div(".hero-wrapper")[
        h.div(".hero-center")[
            h.div(".hero-title")[
                h.span(".hero-comment")["// "],
                h.span(".hero-wordmark")["BlocketAPI"],
            ],
            h.p(".hero-subtitle")[
                "The unofficial API for ",
                h.span(".hero-accent")["blocket.se"],
            ],
            h.p(".hero-desc")["Search cars, boats, motorcycles and general listings.",],
            install_block(),
            h.div(".hero-links")[
                h.a(href=url_for("quickstart"), **_htmx("quickstart"))["Quickstart →"],
                h.a(href=SWAGGER, target="_blank")["Swagger ↗"],
                h.a(href=GITHUB, target="_blank")["GitHub ↗"],
            ],
        ],
    ]


def search_boat_code() -> h.Node:
    return code_block(
        "boats.py",
        "PY",
        """\
from blocket_api import BlocketAPI, Location

api = BlocketAPI()
boats = api.search_boat(
    locations=[Location.STOCKHOLM],
    price_to=150000,
)

for boat in boats["docs"]:
    print(boat["heading"], boat["price"]["amount"])""",
    )


def search_mc_code() -> h.Node:
    return code_block(
        "mc.py",
        "PY",
        """\
from blocket_api import BlocketAPI, Location, McSortOrder

api = BlocketAPI()
bikes = api.search_mc(
    locations=[Location.STOCKHOLM],
    sort_order=McSortOrder.PRICE_ASC,
    price_to=50000,
)

for bike in bikes["docs"]:
    print(bike["heading"], bike["price"]["amount"])""",
    )


def examples_section() -> h.Node:
    return h.section(".section.section-alt")[
        h.div(".container")[
            h.div(".section-header")[h.h2["Common patterns"],],
            h.div(".examples-tabs")[
                h.div(".examples-tab-bar")[
                    h.button(
                        ".ex-tab.active", onclick="switchExTab(this,'ext-general')"
                    )["General search"],
                    h.button(".ex-tab", onclick="switchExTab(this,'ext-car')")["Cars"],
                    h.button(".ex-tab", onclick="switchExTab(this,'ext-boat')")[
                        "Boats"
                    ],
                    h.button(".ex-tab", onclick="switchExTab(this,'ext-mc')")[
                        "Motorcycles"
                    ],
                    h.button(".ex-tab", onclick="switchExTab(this,'ext-alert')")[
                        "Price alert"
                    ],
                ],
                h.div(".ex-tab-panel.active", id="ext-general")[
                    code_tabs(
                        ("Python", hero_code()),
                        (
                            "cURL",
                            code_block(
                                "terminal",
                                "SH",
                                f'curl "{API_BASE}/v1/search?query=iPhone+15"',
                            ),
                        ),
                    ),
                    h.p(".example-panel-note")[
                        h.a(".link", href=url_for("quickstart"), **_htmx("quickstart"))[
                            "Quickstart →"
                        ]
                    ],
                ],
                h.div(".ex-tab-panel", id="ext-car")[
                    code_tabs(
                        ("Python", car_code()),
                        (
                            "cURL",
                            code_block(
                                "terminal",
                                "SH",
                                f'curl "{API_BASE}/v1/search/car?models=VOLVO&locations=STOCKHOLM&price_to=80000&year_from=2018&sort_order=PRICE_ASC"',
                            ),
                        ),
                    ),
                    h.p(".example-panel-note")[
                        "10+ filters: model, year, transmission, wheel drive, mileage. ",
                        h.a(
                            ".link",
                            href=url_for("endpoints") + "#search-car",
                            **_htmx("endpoints"),
                        )["All parameters →"],
                    ],
                ],
                h.div(".ex-tab-panel", id="ext-boat")[
                    code_tabs(
                        ("Python", search_boat_code()),
                        (
                            "cURL",
                            code_block(
                                "terminal",
                                "SH",
                                f'curl "{API_BASE}/v1/search/boat?locations=STOCKHOLM&price_to=150000"',
                            ),
                        ),
                    ),
                    h.p(".example-panel-note")[
                        h.a(
                            ".link",
                            href=url_for("endpoints") + "#search-boat",
                            **_htmx("endpoints"),
                        )["All parameters →"]
                    ],
                ],
                h.div(".ex-tab-panel", id="ext-mc")[
                    code_tabs(
                        ("Python", search_mc_code()),
                        (
                            "cURL",
                            code_block(
                                "terminal",
                                "SH",
                                f'curl "{API_BASE}/v1/search/mc?locations=STOCKHOLM&price_to=50000&sort_order=PRICE_ASC"',
                            ),
                        ),
                    ),
                    h.p(".example-panel-note")[
                        h.a(
                            ".link",
                            href=url_for("endpoints") + "#search-mc",
                            **_htmx("endpoints"),
                        )["All parameters →"]
                    ],
                ],
                h.div(".ex-tab-panel", id="ext-alert")[
                    code_tabs(
                        ("Python", alert_code()),
                        (
                            "cURL",
                            code_block(
                                "terminal",
                                "SH",
                                f"curl -s \"{API_BASE}/v1/search?query=Sony+WH-1000XM5&sort_order=PRICE_ASC\" \\\n  | jq '.docs[] | select(.price.amount <= 1800)'",
                            ),
                        ),
                    ),
                    h.p(".example-panel-note")[
                        h.a(".link", href=url_for("quickstart"), **_htmx("quickstart"))[
                            "Quickstart →"
                        ]
                    ],
                ],
            ],
        ],
    ]


def feature(icon: str, title: str, desc: str) -> h.Node:
    return h.div(".feature-cell")[
        h.div(".feature-icon")[icon],
        h.div[
            h.h3(".feature-title")[title],
            h.p(".feature-desc")[desc],
        ],
    ]


def features() -> h.Node:
    return h.section(".section.section-alt")[
        h.div(".container")[
            h.div(".section-header")[
                h.span(".section-label")["What you get"],
                h.h2["Built for automation"],
            ],
            h.div(".feature-grid")[
                feature(
                    "🔌",
                    "REST API",
                    f"GET {API_BASE}/v1/search — works from any language, any HTTP client.",
                ),
                feature(
                    "🐍",
                    "Python library",
                    "Typed enums for models, locations, sort orders. No string guessing.",
                ),
                feature(
                    "🚗",
                    "Vehicle search",
                    "Cars, motorcycles, and boats each have dedicated endpoints with rich filters.",
                ),
                feature(
                    "📄",
                    "Consistent JSON",
                    "Every endpoint returns docs[], total, query. Predictable, easy to parse.",
                ),
                feature(
                    "⚡",
                    "No auth overhead",
                    "No tokens to refresh, no rate-limit headers to track, no signup flow.",
                ),
                feature(
                    "📦",
                    "uv compatible",
                    "Inline script metadata — ship a single .py file with zero setup.",
                ),
            ],
        ],
    ]


def uv_section() -> h.Node:
    return h.section(".section")[
        h.div(".container")[
            h.div(".uv-grid")[
                h.div[
                    h.span(".section-label")["Zero setup"],
                    h.h2(".uv-heading")[
                        "One file. ",
                        h.span(".gradient-text")["No venv."],
                    ],
                    h.p(".uv-desc")[
                        "Add a ",
                        ic("# /// script"),
                        " block and ",
                        ic("uv run"),
                        " handles dependencies automatically. No ",
                        ic("pyproject.toml"),
                        ", no activation, no friction.",
                    ],
                    h.div(".check-list")[
                        h.div(".check-item")[
                            h.span(".check")["✓"], " Deps install in milliseconds"
                        ],
                        h.div(".check-item")[
                            h.span(".check")["✓"], " Single file, shareable anywhere"
                        ],
                        h.div(".check-item")[
                            h.span(".check")["✓"], " Perfect for cron jobs"
                        ],
                    ],
                    h.div(".btn-row")[
                        h.a(
                            ".btn.btn-primary",
                            href=url_for("quickstart"),
                            **_htmx("quickstart"),
                        )["Quickstart →"],
                        h.a(
                            ".btn.btn-secondary",
                            href=url_for("endpoints"),
                            **_htmx("endpoints"),
                        )["Endpoints"],
                    ],
                ],
                h.div(".uv-code-stack")[
                    uv_inline_code(),
                    uv_run_code(),
                ],
            ],
        ],
    ]


def cta() -> h.Node:
    return h.section(".section.section-cta")[
        h.div(".container")[
            h.div(".cta-terminal")[
                h.span(".cmt")["$ "],
                h.span(".install-prompt")["curl "],
                h.span(".str")[f'"{API_BASE}/v1/search?query=iPhone+15"'],
                h.span(".cmt")[" | python3 -m json.tool"],
            ],
            h.p(".cta-desc")["That's it. No account. No key. Just start."],
            h.div(".hero-actions")[
                h.a(
                    ".btn.btn-primary",
                    href=url_for("quickstart"),
                    **_htmx("quickstart"),
                )["Get started →"],
                h.a(
                    ".btn.btn-secondary",
                    href=url_for("endpoints"),
                    **_htmx("endpoints"),
                )["API reference"],
                h.a(".btn.btn-secondary", href=GITHUB, target="_blank")["GitHub ↗"],
            ],
        ],
    ]
