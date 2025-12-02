import json
import re
from dataclasses import dataclass
from typing import Any

from bs4 import BeautifulSoup, NavigableString, Tag
from httpx import Response

from .constants import SITE_URL


@dataclass(frozen=True)
class RecommerceAd:
    id: int

    @property
    def url(self) -> str:
        return f"{SITE_URL}/recommerce/forsale/item/{self.id}"

    def parse(self, response: Response) -> dict[str, Any]:
        soup = BeautifulSoup(response.content, "html.parser")
        json_script_tag = soup.select_one(
            'script:-soup-contains("window.__staticRouterHydrationData")'
        )
        if not json_script_tag:
            return {}

        if match := re.search(r'JSON\.parse\("(.+)"\)', json_script_tag.text):
            raw_json = match.group(1)
            escaped = raw_json.encode("utf-8").decode("unicode_escape")
            return json.loads(escaped.encode("latin1").decode("utf-8"))
        else:
            return {}


@dataclass(frozen=True)
class MobilityAd:
    id: int

    @property
    def url(self) -> str:
        return f"{SITE_URL}/mobility/item/{self.id}"

    def parse(self, response: Response) -> dict[str, Any]:
        soup = BeautifulSoup(response.content, "html.parser")
        grid = soup.find("div", class_="grid grid-cols-1 md:grid-cols-3 md:gap-x-32")

        if not grid:
            return {}

        data: dict[str, Any] = {"url": self.url}

        self._extract_title_and_subtitle(grid, data)
        self._extract_quick_specs(grid, data)
        self._extract_price(grid, data)
        self._extract_description(grid, data)
        self._extract_specifications(grid, data)
        self._extract_seller_type(soup, data)
        self._extract_ad_id(soup, data)

        self.extend(data, soup, grid)

        return data

    def _extract_title_and_subtitle(self, grid: Tag, data: dict) -> None:
        if title := grid.find("h1", class_=lambda x: x and "t1" in x):
            data["title"] = title.get_text(strip=True)

        if subtitle := grid.find("p", class_=lambda x: x and "s-text-subtle" in x):
            data["subtitle"] = subtitle.get_text(strip=True)

    def _extract_quick_specs(self, grid: Tag, data: dict) -> None:
        if specs_grid := grid.find(
            "div", class_=lambda x: x and "grid" in x and "gap-24" in x
        ):
            for item in specs_grid.find_all("div", class_="flex gap-16 hyphens-auto"):
                label = item.find("span", class_="s-text-subtle")
                value = item.find("p", class_="m-0 font-bold")
                if label and value:
                    label_text = label.get_text(strip=True)
                    value_text = value.get_text(strip=True)
                    key = getattr(self, "quick_spec_mapping", {}).get(
                        label_text, label_text.lower().replace(" ", "_")
                    )
                    data[key] = value_text

    def _extract_price(self, grid: Tag, data: dict) -> None:
        if price_section := grid.find("div", class_="border-t pt-40 mt-40"):
            price_elem = price_section.find("span", class_="t2")
            if price_elem:
                data["price"] = price_elem.get_text(strip=True)

    def _extract_description(self, grid: Tag, data: dict) -> None:
        for section in grid.find_all("section", class_="border-t mt-40 pt-40"):
            h2 = section.find("h2", class_="t3 mb-0")
            if h2 and "beskrivning" in h2.get_text(strip=True).lower():
                desc_div = section.find("div", class_="whitespace-pre-wrap")
                if desc_div:
                    data["description"] = desc_div.get_text(strip=True)
                return

    def _extract_specifications(self, grid: Tag, data: dict) -> None:
        specs_section = grid.find("section", class_="key-info-section")
        if not specs_section:
            return
        dl = specs_section.find("dl")
        if not dl:
            return

        specifications = {}
        for div in dl.find_all("div", style="break-inside:avoid-column"):
            dt = div.find("dt")
            dd = div.find("dd")
            if dt and dd:
                specifications[dt.get_text(strip=True)] = dd.get_text(strip=True)

        if specifications:
            data["specifications"] = specifications

    def _extract_seller_type(self, soup: BeautifulSoup, data: dict) -> None:
        # Look for a div whose class contains "dealer"
        data["seller_type"] = (
            "dealer"
            if soup.find("div", class_=lambda x: x and "dealer" in x.lower())
            else "private"
        )

    def _extract_ad_id(self, soup: BeautifulSoup, data: dict) -> None:
        label = next(
            (
                p
                for p in soup.find_all("p")
                if isinstance(p.string, NavigableString) and "Annons-ID" in p.string
            ),
            None,
        )
        if label:
            elem = label.find_next("p")
            if elem:
                data["ad_id"] = elem.get_text(strip=True)

    def extend(self, data: dict, soup: BeautifulSoup, grid: Tag) -> None:
        pass


class CarAd(MobilityAd):
    quick_spec_mapping = {
        "Modellår": "model_year",
        "Miltal": "mileage",
        "Växellåda": "transmission",
        "Drivmedel": "fuel",
    }

    def extend(self, data: dict, soup: BeautifulSoup, grid: Tag) -> None:
        equip_section = next(
            (
                h2
                for h2 in grid.find_all("h2")
                if isinstance(h2.string, NavigableString) and "Utrustning" in h2.string
            ),
            None,
        )
        if equip_section:
            parent = equip_section.find_parent("section")
            if parent:
                items = [li.get_text(strip=True) for li in parent.find_all("li")]
                if items:
                    data["equipment"] = items


class BoatAd(MobilityAd):
    quick_spec_mapping = {
        "Modellår": "model_year",
        "Längd": "length",
        "Motortyp": "engine_type",
        "Säten": "seats",
    }

    def extend(self, data: dict, soup: BeautifulSoup, grid: Tag) -> None:
        if place_h2 := soup.find(
            "h2", text=lambda t: isinstance(t, NavigableString) and "Plats" in t
        ):
            if link := place_h2.find_parent():
                data["location"] = link.get_text(strip=True)


class McAd(MobilityAd):
    quick_spec_mapping = {
        "Modellår": "model_year",
        "Motorvolym": "engine_volume",
        "Typ": "type",
    }

    def extend(self, data: dict, soup: BeautifulSoup, grid: Tag) -> None:
        if place_h2 := soup.find(
            "h2", text=lambda t: isinstance(t, NavigableString) and "Plats" in t
        ):
            if link := place_h2.find_parent():
                data["location"] = link.get_text(strip=True)
