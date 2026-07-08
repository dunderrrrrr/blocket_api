import htpy as h
from flask import url_for

from docs.components_base import (
    _htmx,
    code_block,
    ic,
    sidebar_link,
    sidebar_section,
    tip_box,
)

# ── Sidebar ───────────────────────────────────────────────────────────────────


def sidebar():
    return [
        sidebar_section(
            "Tips",
            [
                sidebar_link("Run with uv", "#uv", active=True),
                sidebar_link("Cron scheduling", "#cron"),
                sidebar_link("Pagination", "#pagination"),
                sidebar_link("Sorting & filters", "#sorting"),
                sidebar_link("Multi-location", "#location"),
                sidebar_link("Org ID filtering", "#orgid"),
                sidebar_link("Market analysis", "#analysis"),
            ],
        ),
        sidebar_section(
            "Reference",
            [
                sidebar_link("Quickstart", url_for("quickstart")),
                sidebar_link("Endpoints", url_for("endpoints")),
                sidebar_link("Examples", url_for("examples")),
            ],
        ),
    ]


# ── Code snippets ─────────────────────────────────────────────────────────────


def uv_global():
    return code_block(
        "terminal",
        "SH",
        [
            h.span(".cmt")["# install uv globally"],
            "\n",
            "curl -LsSf https://astral.sh/uv/install.sh | sh\n\n",
            h.span(".cmt")["# run any blocket script with zero setup"],
            "\n",
            "uv run my_search.py",
        ],
    )


def uv_inline():
    return code_block(
        "script.py",
        "PY",
        [
            h.span(".cmt")["# /// script"],
            "\n",
            h.span(".cmt")['# requires-python = ">=3.10"'],
            "\n",
            h.span(".cmt")['# dependencies = ["blocket-api"]'],
            "\n",
            h.span(".cmt")["# ///"],
            "\n\n",
            h.span(".kw")["from"],
            " blocket_api ",
            h.span(".kw")["import"],
            " ",
            h.span(".cls")["BlocketAPI"],
            "\n\n",
            "api ",
            h.span(".op")["="],
            " ",
            h.span(".cls")["BlocketAPI"],
            "()\n",
            "results ",
            h.span(".op")["="],
            " api.",
            h.span(".fn")["search"],
            "(",
            h.span(".str")['"Lego"'],
            ")\n",
            h.span(".fn")["print"],
            "(results[",
            h.span(".str")['"docs"'],
            "][",
            h.span(".num")["0"],
            "][",
            h.span(".str")['"heading"'],
            "])",
        ],
    )


def cron():
    return code_block(
        "crontab -e",
        "SH",
        [
            h.span(".cmt")["# run price alert every 15 minutes"],
            "\n",
            "*/15 * * * * /usr/local/bin/uv run /home/user/price_alert.py >> /tmp/blocket.log 2>&1\n\n",
            h.span(".cmt")["# daily full scan at 08:00"],
            "\n",
            "0 8 * * * /usr/local/bin/uv run /home/user/daily_scan.py",
        ],
    )


def pagination():
    return code_block(
        "paginate_all.py",
        "PY",
        [
            h.span(".kw")["from"],
            " blocket_api ",
            h.span(".kw")["import"],
            " ",
            h.span(".cls")["BlocketAPI"],
            "\n\n",
            "api ",
            h.span(".op")["="],
            " ",
            h.span(".cls")["BlocketAPI"],
            "()\n",
            "all_docs ",
            h.span(".op")["="],
            " []\npage ",
            h.span(".op")["="],
            " ",
            h.span(".num")["0"],
            "\n\n",
            h.span(".kw")["while"],
            " ",
            h.span(".kw")["True"],
            ":\n",
            "    batch ",
            h.span(".op")["="],
            " api.",
            h.span(".fn")["search"],
            "(",
            h.span(".str")['"MacBook"'],
            ", page",
            h.span(".op")["="],
            "page)[",
            h.span(".str")['"docs"'],
            "]\n",
            "    ",
            h.span(".kw")["if"],
            " ",
            h.span(".kw")["not"],
            " batch:\n        ",
            h.span(".kw")["break"],
            "\n",
            "    all_docs.",
            h.span(".fn")["extend"],
            "(batch)\n    page ",
            h.span(".op")["+="],
            " ",
            h.span(".num")["1"],
            "\n\n",
            h.span(".fn")["print"],
            '(f"Total: {len(all_docs)} listings")',
        ],
    )


def sort_filter():
    return code_block(
        "sort_tip.py",
        "PY",
        [
            h.span(".kw")["from"],
            " blocket_api ",
            h.span(".kw")["import"],
            " ",
            h.span(".cls")["BlocketAPI"],
            ", ",
            h.span(".cls")["CarSortOrder"],
            "\n\n",
            "api ",
            h.span(".op")["="],
            " ",
            h.span(".cls")["BlocketAPI"],
            "()\n",
            "cars ",
            h.span(".op")["="],
            " api.",
            h.span(".fn")["search_car"],
            "(\n",
            "    sort_order",
            h.span(".op")["="],
            h.span(".cls")["CarSortOrder"],
            ".",
            h.span(".var")["PRICE_ASC"],
            ",\n",
            "    price_to",
            h.span(".op")["="],
            h.span(".num")["100000"],
            ",\n)\n",
        ],
    )


def multi_location():
    return code_block(
        "multi_location.py",
        "PY",
        [
            h.span(".kw")["from"],
            " blocket_api ",
            h.span(".kw")["import"],
            " ",
            h.span(".cls")["BlocketAPI"],
            ", ",
            h.span(".cls")["Location"],
            "\n\n",
            "api ",
            h.span(".op")["="],
            " ",
            h.span(".cls")["BlocketAPI"],
            "()\n",
            "results ",
            h.span(".op")["="],
            " api.",
            h.span(".fn")["search_car"],
            "(\n",
            "    locations",
            h.span(".op")["="],
            "[\n",
            "        ",
            h.span(".cls")["Location"],
            ".",
            h.span(".var")["STOCKHOLM"],
            ",\n",
            "        ",
            h.span(".cls")["Location"],
            ".",
            h.span(".var")["GOTHENBURG"],
            ",\n",
            "        ",
            h.span(".cls")["Location"],
            ".",
            h.span(".var")["MALMO"],
            ",\n",
            "    ],\n)\n",
        ],
    )


def org_id():
    return code_block(
        "org_id_scan.py",
        "PY",
        [
            h.span(".kw")["from"],
            " blocket_api ",
            h.span(".kw")["import"],
            " ",
            h.span(".cls")["BlocketAPI"],
            "\n\n",
            "api ",
            h.span(".op")["="],
            " ",
            h.span(".cls")["BlocketAPI"],
            "()\n",
            "dealer_ads ",
            h.span(".op")["="],
            " api.",
            h.span(".fn")["search"],
            "(",
            h.span(".str")['"iPhone"'],
            ", org_id",
            h.span(".op")["="],
            h.span(".str")['"67890"'],
            ")\n",
            h.span(".fn")["print"],
            '(f"{len(dealer_ads[',
            h.span(".str")['"docs"'],
            '])} ads from this seller")',
        ],
    )


def median_price():
    return code_block(
        "median_price.py",
        "PY",
        [
            h.span(".cmt")["# /// script"],
            "\n",
            h.span(".cmt")['# dependencies = ["blocket-api", "statistics"]'],
            "\n",
            h.span(".cmt")["# ///"],
            "\n\n",
            h.span(".kw")["import"],
            " statistics\n",
            h.span(".kw")["from"],
            " blocket_api ",
            h.span(".kw")["import"],
            " ",
            h.span(".cls")["BlocketAPI"],
            ", ",
            h.span(".cls")["CarModel"],
            "\n\n",
            "api ",
            h.span(".op")["="],
            " ",
            h.span(".cls")["BlocketAPI"],
            "()\n",
            "cars ",
            h.span(".op")["="],
            " api.",
            h.span(".fn")["search_car"],
            "(models",
            h.span(".op")["="],
            "[",
            h.span(".cls")["CarModel"],
            ".",
            h.span(".var")["TESLA"],
            "])\n\n",
            "prices ",
            h.span(".op")["="],
            " [d.",
            h.span(".fn")["get"],
            "(",
            h.span(".str")['"price"'],
            ", {}).",
            h.span(".fn")["get"],
            "(",
            h.span(".str")['"amount"'],
            ") ",
            h.span(".kw")["for"],
            " d ",
            h.span(".kw")["in"],
            " cars[",
            h.span(".str")['"docs"'],
            "] ",
            h.span(".kw")["if"],
            " d.",
            h.span(".fn")["get"],
            "(",
            h.span(".str")['"price"'],
            ")]\n\n",
            h.span(".fn")["print"],
            '(f"Median: {statistics.',
            h.span(".fn")["median"],
            '(prices):,.0f} SEK")',
        ],
    )


# ── Page sections ─────────────────────────────────────────────────────────────


def uv_tip():
    return [
        h.h2(id="uv")["Run scripts with uv"],
        h.p[
            h.a(".link", href="https://github.com/astral-sh/uv", target="_blank")["uv"],
            " is an ultra-fast Python package manager. Use PEP 723 inline script metadata to declare "
            "dependencies inside your file — no setup required.",
        ],
        uv_global(),
        uv_inline(),
        tip_box(
            "🚀",
            [
                "Share scripts with colleagues by copying a single file — ",
                ic("uv run script.py"),
                " handles everything.",
            ],
            kind="tip",
        ),
    ]


def cron_tip():
    return [
        h.h2(".section-h2", id="cron")["Schedule with cron"],
        h.p[
            "Automate your scripts with cron. Always use the full path to ",
            ic("uv"),
            " so cron can find it.",
        ],
        cron(),
        tip_box(
            "💡",
            [
                "Find where uv is installed with ",
                ic("which uv"),
                ". Use that full path in your crontab to avoid PATH issues.",
            ],
        ),
    ]


def pagination_tip():
    return [
        h.h2(".section-h2", id="pagination")["Pagination"],
        h.p[
            "By default, ",
            ic("search()"),
            " returns up to 40 results. Paginate by passing an incrementing ",
            ic("page"),
            " parameter.",
        ],
        pagination(),
        tip_box(
            "⚠️",
            [
                "Be courteous — add a small delay between pages: ",
                ic("import time; time.sleep(0.5)"),
                ".",
            ],
            kind="warning",
        ),
    ]


def sorting_tip():
    return [
        h.h2(".section-h2", id="sorting")["Sorting & price filters"],
        h.p[
            "Combine ",
            ic("sort_order"),
            " with ",
            ic("price_from"),
            " / ",
            ic("price_to"),
            " to find deals fast.",
        ],
        sort_filter(),
        h.div(".endpoint-table")[
            h.table[
                h.thead[h.tr[h.th["Sort value"], h.th["Meaning"]]],
                h.tbody[
                    h.tr[h.td[ic("PRICE_ASC")], h.td["Cheapest first"]],
                    h.tr[h.td[ic("PRICE_DESC")], h.td["Most expensive first"]],
                    h.tr[h.td[ic("DATE_ASC")], h.td["Oldest first"]],
                    h.tr[h.td[ic("DATE_DESC")], h.td["Newest first (default)"]],
                    h.tr[
                        h.td[ic("MILEAGE_ASC")],
                        h.td["Lowest mileage first (cars only)"],
                    ],
                ],
            ]
        ],
    ]


def location_tip():
    return [
        h.h2(".section-h2", id="location")["Multi-location search"],
        h.p[
            "Pass a list of ",
            ic("Location"),
            " values to search across multiple Swedish counties simultaneously.",
        ],
        multi_location(),
    ]


def orgid_tip():
    return [
        h.h2(".section-h2", id="orgid")["Filter by dealer (org_id)"],
        h.p[
            "Use the ",
            ic("org_id"),
            " parameter to fetch all ads from a specific dealer. "
            "You can find a seller's org_id by inspecting a listing on Blocket.se.",
        ],
        org_id(),
    ]


def analysis_tip():
    return [
        h.h2(".section-h2", id="analysis")["Market analysis & price stats"],
        h.p[
            "Use the ",
            ic("statistics"),
            " or ",
            ic("pandas"),
            " standard libraries to compute market insights.",
        ],
        median_price(),
        code_block(
            "terminal",
            "SH",
            [
                "uv run median_price.py\n",
                h.span(".cmt")["# Median Tesla price: 389 000 SEK"],
            ],
        ),
        h.div(".btn-row")[
            h.a(".btn.btn-primary", href=url_for("examples"), **_htmx("examples"))[
                "Browse full examples →"
            ],
            h.a(".btn.btn-secondary", href=url_for("endpoints"), **_htmx("endpoints"))[
                "Endpoint reference"
            ],
        ],
    ]
