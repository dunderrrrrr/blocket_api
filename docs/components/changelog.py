import re
from datetime import datetime

import htpy as h

_BADGE_CLASS = {
    "feat": "badge-feat",
    "fix": "badge-fix",
    "refactor": "badge-refactor",
    "docs": "badge-docs",
    "perf": "badge-perf",
    "chore": "badge-refactor",
}

_SKIP_LABELS = {"dependencies"}


def _parse_type(title: str) -> tuple[str, str]:
    """Return (kind, clean_title) from a conventional-commit PR title."""
    m = re.match(r"^(\w+)(?:\([^)]+\))?[!]?:\s*(.+)$", title)
    if m:
        return m.group(1).lower(), m.group(2).strip()
    return "feat", title.strip()


def _badge(kind: str) -> h.Node:
    cls = _BADGE_CLASS.get(kind, "badge-feat")
    return h.span(f".badge.{cls}")[kind]


def _pr_row(pr: dict) -> h.Node:
    kind, title = _parse_type(pr["title"])
    date = datetime.fromisoformat(pr["merged_at"].replace("Z", "+00:00"))
    user = pr.get("user", {})
    first_body_line = (pr.get("body") or "").strip().split("\n")[0].strip()
    return h.div(".changelog-entry")[
        h.div(".changelog-line")[h.div(".changelog-dot")],
        h.div(".changelog-body")[
            h.div(".changelog-meta")[
                _badge(kind),
                h.span(".changelog-date")[date.strftime("%Y-%m-%d")],
                h.a(".changelog-ref", href=pr["html_url"], target="_blank")[
                    f"#{pr['number']} ↗"
                ],
                h.a(
                    ".changelog-author", href=user.get("html_url", "#"), target="_blank"
                )[
                    h.img(
                        ".changelog-avatar",
                        src=user.get("avatar_url", ""),
                        alt=user.get("login", ""),
                    ),
                    user.get("login", ""),
                ],
            ],
            h.p(".changelog-title")[title],
            h.p(".changelog-desc")[first_body_line] if first_body_line else "",
        ],
    ]


def render(prs: list) -> h.Node:
    merged = [
        pr
        for pr in prs
        if pr.get("merged_at")
        and not any(lbl["name"] in _SKIP_LABELS for lbl in pr.get("labels", []))
    ]

    if not merged:
        return h.p["No releases found."]

    by_year: dict[int, list] = {}
    for pr in merged:
        year = datetime.fromisoformat(pr["merged_at"].replace("Z", "+00:00")).year
        by_year.setdefault(year, []).append(pr)

    sections = [
        h.div(".changelog-year-group")[
            h.h3(".changelog-year")[str(year)],
            h.div(".changelog-timeline")[[_pr_row(pr) for pr in prs]],
        ]
        for year, prs in sorted(by_year.items(), reverse=True)
    ]

    return h.div[sections]
