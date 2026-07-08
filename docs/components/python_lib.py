import htpy as h
from flask import url_for

from docs.components_base import (
    API_BASE,
    GITHUB,
    PYPI,
    code_block,
    code_tabs,
    ic,
    sidebar_link,
    sidebar_section,
    tip_box,
)


def search_py():
    return code_block(
        "search.py",
        "PY",
        """\
from blocket_api import BlocketAPI, Location, SortOrder

api = BlocketAPI()
results = api.search(
    "iPhone 15",
    sort_order=SortOrder.PRICE_ASC,
    locations=[Location.STOCKHOLM],
)

for item in results["docs"]:
    print(item["heading"], item["price"]["amount"])""",
    )


def search_curl():
    return code_block(
        "terminal",
        "SH",
        f'curl "{API_BASE}/v1/search?query=iPhone+15&sort_order=PRICE_ASC&locations=STOCKHOLM"',
    )


def search_car_py():
    return code_block(
        "search_car.py",
        "PY",
        """\
from blocket_api import (
    BlocketAPI, CarModel, CarSortOrder,
    CarTransmission, Location,
)

api = BlocketAPI()
cars = api.search_car(
    models=[CarModel.VOLVO],
    locations=[Location.STOCKHOLM],
    transmissions=[CarTransmission.AUTOMATIC],
    sort_order=CarSortOrder.PRICE_ASC,
    price_to=200000,
    year_from=2018,
)

for car in cars["docs"]:
    print(car["heading"], car["price"]["amount"], "SEK")""",
    )


def search_car_curl():
    return code_block(
        "terminal",
        "SH",
        f'curl "{API_BASE}/v1/search/car?models=VOLVO&locations=STOCKHOLM&transmissions=AUTOMATIC&price_to=200000&year_from=2018&sort_order=PRICE_ASC"',
    )


def search_boat_py():
    return code_block(
        "search_boat.py",
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


def search_boat_curl():
    return code_block(
        "terminal",
        "SH",
        f'curl "{API_BASE}/v1/search/boat?locations=STOCKHOLM&price_to=150000"',
    )


def search_mc_py():
    return code_block(
        "search_mc.py",
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


def search_mc_curl():
    return code_block(
        "terminal",
        "SH",
        f'curl "{API_BASE}/v1/search/mc?locations=STOCKHOLM&price_to=50000&sort_order=PRICE_ASC"',
    )


def get_ad_py():
    return code_block(
        "get_ad.py",
        "PY",
        """\
from blocket_api import BlocketAPI

api = BlocketAPI()

# first get a listing from any search
results = api.search_car(models=[...])
ad_ref = results["docs"][0]

# fetch full ad detail
detail = api.get_ad(ad_ref)
print(detail)""",
    )


def get_ad_curl():
    return code_block("terminal", "SH", f'curl "{API_BASE}/v1/ad/car?id=12345678"')


def method_card(
    id_: str, signature: str, desc: str, params: list[tuple[str, str, str]], *blocks
):
    return h.div(".example-full-card", id=id_)[
        h.div(".example-card-header")[
            h.div(".example-card-icon")[h.code(".ep-path")[signature]],
        ],
        h.div(".example-card-body")[
            h.p(".ep-summary")[desc],
            h.div(".endpoint-table")[
                h.table[
                    h.thead[h.tr[h.th["Parameter"], h.th["Type"], h.th["Notes"]]],
                    h.tbody[
                        [
                            h.tr[
                                h.td[h.code[name]],
                                h.td(".type-code")[typ],
                                h.td[note],
                            ]
                            for name, typ, note in params
                        ]
                    ],
                ]
            ],
            blocks,
        ],
    ]


def sidebar():
    return [
        sidebar_section(
            "Methods",
            [
                sidebar_link("api.search()", "#search", active=True),
                sidebar_link("api.search_car()", "#search-car"),
                sidebar_link("api.search_boat()", "#search-boat"),
                sidebar_link("api.search_mc()", "#search-mc"),
                sidebar_link("api.get_ad()", "#get-ad"),
            ],
        ),
        sidebar_section(
            "Links",
            [
                sidebar_link("PyPI", PYPI),
                sidebar_link("GitHub", GITHUB),
                sidebar_link("Endpoints", url_for("endpoints")),
            ],
        ),
    ]


def install_section():
    return [
        h.h2(id="install")["Installation"],
        h.p["Install via ", ic("uv"), " or ", ic("pip"), ":"],
        code_tabs(
            ("uv", code_block("terminal", "SH", "uv add blocket-api")),
            ("pip", code_block("terminal", "SH", "pip install blocket-api")),
        ),
        tip_box(
            "📦",
            [
                "Available on ",
                h.a(".link", href=PYPI, target="_blank")["PyPI ↗"],
                ". Source on ",
                h.a(".link", href=GITHUB, target="_blank")["GitHub ↗"],
                ".",
            ],
        ),
    ]


def methods_section():
    return [
        h.h2(".section-h2", id="methods")["Methods"],
        method_card(
            "search",
            "api.search(query, **kwargs)",
            "Search all categories by keyword.",
            [
                ("query", "str", "Search term (required)"),
                ("sort_order", "SortOrder", "RELEVANCE, PRICE_ASC, PRICE_DESC, …"),
                ("locations", "list[Location]", "Filter by county"),
                ("page", "int", "Page number, default 1"),
                ("category", "Category", "Top-level category filter"),
            ],
            code_tabs(("Python", search_py()), ("cURL", search_curl())),
        ),
        method_card(
            "search-car",
            "api.search_car(**kwargs)",
            "Search used cars with vehicle-specific filters.",
            [
                ("models", "list[CarModel]", "Make/model enum values"),
                ("locations", "list[Location]", "Filter by county"),
                ("price_from", "int", "Minimum price (SEK)"),
                ("price_to", "int", "Maximum price (SEK)"),
                ("year_from", "int", "Earliest model year"),
                ("year_to", "int", "Latest model year"),
                ("milage_from", "int", "Minimum mileage (km)"),
                ("milage_to", "int", "Maximum mileage (km)"),
                ("transmissions", "list[CarTransmission]", "AUTOMATIC or MANUAL"),
                ("wheel_drive", "list[CarWheelDrive]", "FWD, RWD, AWD, …"),
                ("colors", "list[CarColor]", "Exterior colour"),
                ("horsepower_from", "int", "Min horsepower"),
                ("horsepower_to", "int", "Max horsepower"),
                ("org_id", "int", "Filter by dealer org ID"),
                ("sort_order", "CarSortOrder", "PRICE_ASC, PRICE_DESC, …"),
            ],
            code_tabs(("Python", search_car_py()), ("cURL", search_car_curl())),
        ),
        method_card(
            "search-boat",
            "api.search_boat(**kwargs)",
            "Search used boats.",
            [
                ("types", "list[BoatType]", "Boat class (BOWRIDER, DAYCRUISER, …)"),
                ("locations", "list[Location]", "Filter by county"),
                ("price_from", "int", "Minimum price (SEK)"),
                ("price_to", "int", "Maximum price (SEK)"),
                ("length_from", "int", "Min length (feet)"),
                ("length_to", "int", "Max length (feet)"),
                ("org_id", "int", "Filter by dealer org ID"),
                ("sort_order", "BoatSortOrder", "PRICE_ASC, LENGTH_DESC, …"),
            ],
            code_tabs(("Python", search_boat_py()), ("cURL", search_boat_curl())),
        ),
        method_card(
            "search-mc",
            "api.search_mc(**kwargs)",
            "Search used motorcycles.",
            [
                ("models", "list[McModel]", "Make/model enum values"),
                ("types", "list[McType]", "ADVENTURE, CHOPPER, …"),
                ("locations", "list[Location]", "Filter by county"),
                ("price_from", "int", "Minimum price (SEK)"),
                ("price_to", "int", "Maximum price (SEK)"),
                ("engine_volume_from", "int", "Min engine volume (cc)"),
                ("engine_volume_to", "int", "Max engine volume (cc)"),
                ("org_id", "int", "Filter by dealer org ID"),
                ("sort_order", "McSortOrder", "PRICE_ASC, MILAGE_DESC, …"),
            ],
            code_tabs(("Python", search_mc_py()), ("cURL", search_mc_curl())),
        ),
        method_card(
            "get-ad",
            "api.get_ad(ad)",
            "Fetch full detail for a single listing returned from any search.",
            [
                (
                    "ad",
                    "RecommerceAd | CarAd | BoatAd | McAd",
                    "Ad object from a search result",
                ),
            ],
            code_tabs(("Python", get_ad_py()), ("cURL", get_ad_curl())),
        ),
    ]
