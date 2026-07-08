import httpx
from flask import Flask, Response

from docs.views import changelog, endpoints, index, python, quickstart

app = Flask(__name__, static_folder="static")

app.add_url_rule("/", "index", index.view)
app.add_url_rule("/quickstart", "quickstart", quickstart.view)
app.add_url_rule("/python", "python", python.view)
app.add_url_rule("/endpoints", "endpoints", endpoints.view)
app.add_url_rule("/changelog", "changelog", changelog.view)

app.add_url_rule("/_/index", "index_fragment", index.fragment_view)
app.add_url_rule("/_/quickstart", "quickstart_fragment", quickstart.fragment_view)
app.add_url_rule("/_/python", "python_fragment", python.fragment_view)
app.add_url_rule("/_/endpoints", "endpoints_fragment", endpoints.fragment_view)
app.add_url_rule("/_/changelog", "changelog_fragment", changelog.fragment_view)


def endpoints_body() -> str:
    from docs.components import endpoints as ep_c

    spec = httpx.get("https://blocket-api.se/swagger/openapi.json", timeout=10).json()
    return str(ep_c.render(spec))


app.add_url_rule("/_/endpoints-body", "endpoints_body", endpoints_body)


def robots_txt() -> Response:
    body = (
        "User-agent: *\n"
        "Allow: /\n"
        "Disallow: /_/\n"
        "\n"
        "Sitemap: https://blocket-api.se/sitemap.xml\n"
    )
    return Response(body, mimetype="text/plain")


app.add_url_rule("/robots.txt", "robots_txt", robots_txt)


def sitemap_xml() -> Response:
    from docs.components_base import SITE_ROOT

    pages = ["", "/quickstart", "/python", "/endpoints", "/changelog"]
    urls = "\n".join(f"  <url><loc>{SITE_ROOT}{p}</loc></url>" for p in pages)
    body = f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n'
    return Response(body, mimetype="application/xml")


app.add_url_rule("/sitemap.xml", "sitemap_xml", sitemap_xml)


def changelog_body() -> str:
    from docs.components import changelog as cl_c

    prs = httpx.get(
        "https://api.github.com/repos/dunderrrrrr/blocket_api/pulls",
        params={"state": "closed", "per_page": 100},
        timeout=10,
    ).json()
    return str(cl_c.render(prs))


app.add_url_rule("/_/changelog-body", "changelog_body", changelog_body)

if __name__ == "__main__":
    app.run(debug=True)
