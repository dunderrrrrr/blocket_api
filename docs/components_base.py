"""Shared htpy components. All pages are rendered via page()."""

import json
import threading
import time
import urllib.request
from collections.abc import Callable

import htpy as h
from flask import url_for
from markupsafe import Markup

_gh_cache: dict = {}
_gh_lock = threading.Lock()


def _gh_stats() -> dict:
    now = time.time()
    with _gh_lock:
        if _gh_cache.get("ts", 0) + 300 > now:
            return _gh_cache
    try:
        with urllib.request.urlopen(
            "https://api.github.com/repos/dunderrrrrr/blocket_api", timeout=3
        ) as r:
            data = json.loads(r.read())
        result = {
            "stars": data.get("stargazers_count", 0),
            "forks": data.get("forks_count", 0),
            "version": None,
            "ts": now,
        }
    except Exception:
        result = {**_gh_cache, "ts": now}
    try:
        with urllib.request.urlopen(
            "https://api.github.com/repos/dunderrrrrr/blocket_api/releases/latest",
            timeout=3,
        ) as r:
            data = json.loads(r.read())
        result["version"] = data.get("tag_name")
    except Exception:
        pass
    with _gh_lock:
        _gh_cache.update(result)
    return result


API_BASE = "https://blocket-api.se"
GITHUB = "https://github.com/dunderrrrrr/blocket_api"
PYPI = "https://pypi.org/project/blocket-api/"
SWAGGER = f"{API_BASE}/swagger"

_NAV_PAGES = [
    ("index", "Home"),
    ("quickstart", "Quickstart"),
    ("python", "Python"),
    ("endpoints", "Endpoints"),
    ("changelog", "Changelog"),
]


# ── Nav ───────────────────────────────────────────────────────────────────────


_LOGO_SVG = Markup(
    '<svg width="22" height="22" viewBox="0 0 24 24" fill="none">'
    '<rect width="24" height="24" rx="6" fill="#e02b20"/>'
    '<path d="M7 8h10M7 12h7M7 16h5" stroke="white" stroke-width="2" stroke-linecap="round"/>'
    "</svg>"
)


def _htmx(ep: str) -> dict:
    """Return htmx attributes for an internal page endpoint name."""
    return dict(
        hx_get=url_for(f"{ep}_fragment"),
        hx_target="#content",
        hx_swap="outerHTML",
        hx_push_url=url_for(ep),
    )


def _logo() -> h.Node:
    return h.a(".nav-logo", href=url_for("index"), **_htmx("index"))[
        _LOGO_SVG,
        h.span["BlocketAPI"],
    ]


def _nav_links(
    active: str = "", mobile: bool = False
) -> tuple[list[h.Element], list[h.Element]]:
    extra = (
        {"onclick": "document.getElementById('mobileMenu').classList.remove('open')"}
        if mobile
        else {}
    )
    internal = [
        h.a(
            ".active" if ep == active else "",
            href=url_for(ep),
            **_htmx(ep),
            **extra,
        )[label]
        for ep, label in _NAV_PAGES
    ]
    external = [
        h.a(".nav-external", href=SWAGGER, target="_blank")["Swagger ↗"],
    ]
    return internal, external


_GH_SVG = Markup(
    '<svg class="gh-badge-svg" viewBox="0 0 448 512" xmlns="http://www.w3.org/2000/svg">'
    '<path d="M439.6 236.1 244 40.5c-5.4-5.5-12.8-8.5-20.4-8.5s-15 3-20.4 8.4L162.5 81l51.5 51.5c27.1-9.1 52.7 16.8 43.4 43.7l49.7 49.7c34.2-11.8 61.2 31 35.5 56.7-26.5 26.5-70.2-2.9-56-37.3L240.3 199v121.9c25.3 12.5 22.3 41.8 9.1 55-6.4 6.4-15.2 10.1-24.3 10.1s-17.8-3.6-24.3-10.1c-17.6-17.6-11.1-46.9 11.2-56v-123c-20.8-8.5-24.6-30.7-18.6-45L142.6 101 8.5 235.1C3 240.6 0 247.9 0 255.5s3 15 8.5 20.4l195.6 195.7c5.4 5.4 12.7 8.4 20.4 8.4s15-3 20.4-8.4l194.7-194.7c5.4-5.4 8.4-12.8 8.4-20.4s-3-15-8.4-20.4"/>'
    "</svg>"
)

# Material Symbols: star, call_split (fork), tag (version)
_ICON_STAR = Markup(
    '<svg class="gh-fact-icon" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M12 17.27 18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/></svg>'
)
_ICON_FORK = Markup(
    '<svg class="gh-fact-icon" viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg"><path d="M5 3.25a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0zm0 2.122a2.25 2.25 0 1 0-1.5 0v.878A2.25 2.25 0 0 0 5.75 8.5h1.5v2.128a2.251 2.251 0 1 0 1.5 0V8.5h1.5a2.25 2.25 0 0 0 2.25-2.25v-.878a2.25 2.25 0 1 0-1.5 0v.878a.75.75 0 0 1-.75.75h-4.5A.75.75 0 0 1 5 6.25v-.878zm3.75 7.378a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0zm3-8.75a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0z"/></svg>'
)
_ICON_TAG = Markup(
    '<svg class="gh-fact-icon" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="m21.41 11.58-9-9A2 2 0 0 0 11 2H4a2 2 0 0 0-2 2v7a2 2 0 0 0 .59 1.42l9 9A2 2 0 0 0 13 22a2 2 0 0 0 1.41-.59l7-7A2 2 0 0 0 22 13a2 2 0 0 0-.59-1.42M5.5 7A1.5 1.5 0 0 1 4 5.5 1.5 1.5 0 0 1 5.5 4 1.5 1.5 0 0 1 7 5.5 1.5 1.5 0 0 1 5.5 7z"/></svg>'
)


def _gh_badges() -> h.Node:
    stats = _gh_stats()
    facts = []
    if stats.get("version"):
        facts.append(h.li(".gh-fact")[_ICON_TAG, stats["version"]])
    if stats.get("stars") is not None:
        facts.append(h.li(".gh-fact")[_ICON_STAR, str(stats["stars"])])
    if stats.get("forks") is not None:
        facts.append(h.li(".gh-fact")[_ICON_FORK, str(stats["forks"])])
    return h.a(".gh-source", href=GITHUB, target="_blank")[
        h.div(".gh-source-icon")[_GH_SVG],
        h.div(".gh-source-info")[
            "GitHub",
            h.ul(".gh-facts")[facts],
        ],
    ]


def nav(active: str = "") -> h.Node:
    internal, external = _nav_links(active)
    return h.nav[
        h.div(".nav-inner")[
            _logo(),
            h.div(".nav-links")[internal],
            h.div(".nav-links.nav-links-right")[external],
            _gh_badges(),
            h.div(".hamburger", onclick="toggleMenu()")[h.span, h.span, h.span],
        ]
    ]


def mobile_menu(active: str = "") -> h.Node:
    internal, external = _nav_links(active, mobile=True)
    return h.div(".mobile-menu", id="mobileMenu")[internal, external]


# ── Footer ────────────────────────────────────────────────────────────────────


def footer() -> h.Node:
    return h.footer[
        h.div(".footer-inner")[
            h.div(".footer-brand")[
                h.a(
                    ".nav-logo",
                    href=url_for("index"),
                    style="display:inline-flex;margin-bottom:.5rem;",
                    **_htmx("index"),
                )[h.span["BlocketAPI"]],
                h.p[
                    "The leading developer API for Blocket.se — Sweden's largest swedish online marketplace. Free to use, open source."
                ],
            ],
            h.div(".footer-col")[
                h.h4["Documentation"],
                [
                    h.a(href=url_for(ep), **_htmx(ep))[label]
                    for ep, label in _NAV_PAGES
                    if ep != "index"
                ],
            ],
            h.div(".footer-col")[
                h.h4["Resources"],
                h.a(href=SWAGGER, target="_blank")["Swagger ↗"],
                h.a(href=GITHUB, target="_blank")["GitHub"],
                h.a(href=PYPI, target="_blank")["PyPI"],
            ],
            h.div(".footer-col")[
                h.h4["Legal"],
                h.a(href=f"{GITHUB}/blob/main/LICENSE", target="_blank")[
                    "License (WTFPL)"
                ],
            ],
        ],
        h.div(".footer-bottom")[
            h.span["© 2024 BlocketAPI. Not affiliated with Blocket AB."],
            h.span["Built for developers, by developers 🇸🇪"],
        ],
    ]


SITE_ROOT = "https://blocket-api.se"
_OG_IMAGE = f"{SITE_ROOT}/static/blocket-api.png"


# ── Page shell ────────────────────────────────────────────────────────────────


def page(
    active: str,
    title: str,
    description: str,
    content_fn: Callable[[], h.Node],
    extra_css: str | None = None,
) -> Markup:
    """Render a full page. content_fn() returns the page body (htpy nodes)."""
    from flask import request

    canonical = SITE_ROOT + request.path

    head_links = [
        h.link(rel="canonical", href=canonical),
        h.link(rel="stylesheet", href=url_for("static", filename="style.css")),
        h.link(rel="preconnect", href="https://fonts.googleapis.com"),
        h.link(rel="preconnect", href="https://fonts.gstatic.com", crossorigin=""),
        h.link(
            href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&family=Space+Mono:wght@400;700&display=swap",
            rel="stylesheet",
        ),
    ]
    if extra_css:
        head_links.append(
            h.link(rel="stylesheet", href=url_for("static", filename=extra_css))
        )

    og_tags = [
        h.meta(property="og:type", content="website"),
        h.meta(property="og:url", content=canonical),
        h.meta(property="og:title", content=title),
        h.meta(property="og:description", content=description),
        h.meta(property="og:image", content=_OG_IMAGE),
        h.meta(property="og:site_name", content="BlocketAPI"),
        h.meta(name="twitter:card", content="summary_large_image"),
        h.meta(name="twitter:title", content=title),
        h.meta(name="twitter:description", content=description),
        h.meta(name="twitter:image", content=_OG_IMAGE),
    ]

    doc = h.html(lang="en")[
        h.head[
            h.meta(charset="UTF-8"),
            h.meta(name="viewport", content="width=device-width, initial-scale=1.0"),
            h.title[title],
            h.meta(name="description", content=description),
            og_tags,
            head_links,
            h.script(src="https://unpkg.com/htmx.org@2.0.4/dist/htmx.min.js", defer=""),
            h.link(
                rel="stylesheet",
                href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.10.0/styles/github.min.css",
            ),
            h.script(
                src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.10.0/highlight.min.js"
            ),
            h.script["hljs.highlightAll();"],
        ],
        h.body[
            nav(active),
            mobile_menu(active),
            h.div(".page-loading-bar", id="page-loading-bar"),
            h.div("#content")[content_fn()],
            footer(),
            h.script(src=url_for("static", filename="main.js")),
        ],
    ]
    return Markup(doc)


def fragment(content_fn: Callable[[], h.Node]) -> str:
    """Render only the inner content nodes — returned for htmx requests."""
    return str(h.div("#content")[content_fn()])


# ── Reusable UI components ────────────────────────────────────────────────────


_LANG_CLASS = {
    "PY": "language-python",
    "SH": "language-bash",
    "JS": "language-javascript",
    "JSON": "language-json",
}


def code_block(filename: str, lang: str, code: str | h.Node) -> h.Node:
    lang_class = _LANG_CLASS.get(lang, "language-plaintext")
    return h.div(".code-block")[
        h.div(".code-header")[
            h.button(".cb-copy", onclick="copyBlock(this)")["Copy"],
            h.span[filename],
        ],
        h.pre[h.code(class_=lang_class)[code]],
    ]


_tab_counter = [0]


def code_tabs(*variants: tuple[str, h.Node]) -> h.Node:
    """Render a tabbed code block with tabs embedded in the code header."""
    _tab_counter[0] += 1
    prefix = f"ct{_tab_counter[0]}"

    btns = [
        h.button(
            ".ct-btn.active" if i == 0 else ".ct-btn",
            onclick=f"switchTab(this,'{prefix}-{i}')",
        )[label]
        for i, (label, _) in enumerate(variants)
    ]

    # Each panel wraps the inner <pre> from the code_block passed in
    panels = [
        h.div(
            ".ct-panel.active" if i == 0 else ".ct-panel",
            id=f"{prefix}-{i}",
        )[block]
        for i, (_, block) in enumerate(variants)
    ]

    return h.div(".code-block.code-tabs-wrap")[
        h.div(".code-header")[
            h.button(".cb-copy", onclick="copyBlock(this)")["Copy"],
            h.div(".ct-group")[btns],
        ],
        panels,
    ]


def tip_box(icon: str, content: h.Node, kind: str = "") -> h.Node:
    return h.div(f".tip.{kind}" if kind else ".tip")[
        h.div(".tip-icon")[icon],
        h.p[content],
    ]


def section_header(label: str, title: str, description: str = "") -> h.Node:
    return h.div(".section-header")[
        h.span(".section-label")[label],
        h.h2[title],
        h.p[description] if description else "",
    ]


def page_hero(title: str, description: str | h.Node, crumb: str) -> h.Node:
    return h.div(".page-hero", style="padding-left:1.5rem;padding-right:1.5rem;")[
        h.div(".breadcrumb")[
            h.a(href=url_for("index"))["Home"],
            h.span["/"],
            crumb,
        ],
        h.h1[title],
        h.p[description] if isinstance(description, str) else description,
    ]


def ic(text: str) -> h.Node:
    """Inline code span."""
    return h.span(".inline-code")[text]


def doc_layout(sidebar_content: h.Node, main_content: h.Node) -> h.Node:
    return h.div(style="max-width:1200px;margin:0 auto;")[
        h.div(".doc-layout")[
            h.aside(".sidebar")[sidebar_content],
            h.main[main_content],
        ]
    ]


def sidebar_section(title: str, links: list[h.Node]) -> h.Node:
    return h.div(".sidebar-section")[
        h.h4[title],
        links,
    ]


def sidebar_link(label: str, href: str, active: bool = False) -> h.Node:
    ep = next(
        (
            ep
            for ep, _ in _NAV_PAGES
            if url_for(ep) == href or url_for(ep) == href.split("#")[0]
        ),
        None,
    )
    is_external = href.startswith("http")
    if ep:
        extra = _htmx(ep)
    elif is_external:
        extra = {"target": "_blank"}
    else:
        extra = {}
    return h.a(
        ".sidebar-link.active" if active else ".sidebar-link", href=href, **extra
    )[label]
