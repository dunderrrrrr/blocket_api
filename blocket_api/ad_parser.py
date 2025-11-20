import json
import re
from dataclasses import dataclass
from typing import Any

from bs4 import BeautifulSoup, Tag
from httpx import Response

from .constants import SITE_URL


@dataclass(frozen=True)
class RecommerceAd:
    id: int

    @property
    def url(self) -> str:
        return f"{SITE_URL}/recommerce/forsale/item/{self.id}"

    def parse(self, response: Response) -> Any:
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
class CarAd:
    id: int

    @property
    def url(self) -> str:
        return f"{SITE_URL}/mobility/item/{self.id}"

    def parse(self, response: Response) -> dict:
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
        self._extract_equipment(grid, data)
        self._extract_seller_type(soup, data)
        self._extract_ad_id(soup, data)

        return data

    def _extract_title_and_subtitle(self, grid: Tag, data: dict[str, Any]) -> None:
        if title := grid.find("h1", class_=lambda x: x and "t1" in x):
            data["title"] = title.get_text(strip=True)

        if subtitle := grid.find(
            "p", class_=lambda x: x and "s-text-subtle" in x and "mt-8" in x
        ):
            data["subtitle"] = subtitle.get_text(strip=True)

    def _extract_quick_specs(self, grid: Tag, data: dict[str, Any]) -> None:
        if specs_grid := grid.find(
            "div", class_=lambda x: x and "grid" in x and "gap-24" in x
        ):
            spec_items = specs_grid.find_all("div", class_="flex gap-16 hyphens-auto")
            for item in spec_items:
                label = item.find("span", class_="s-text-subtle")
                value = item.find("p", class_="m-0 font-bold")
                if label and value:
                    label_text = label.get_text(strip=True)
                    value_text = value.get_text(strip=True)

                    key_mapping = {
                        "Modellår": "model_year",
                        "Miltal": "mileage",
                        "Växellåda": "transmission",
                        "Drivmedel": "fuel",
                    }
                    key = key_mapping.get(
                        label_text, label_text.lower().replace(" ", "_")
                    )
                    data[key] = value_text

    def _extract_price(self, grid: Tag, data: dict[str, Any]) -> None:
        if price_section := grid.find("div", class_="border-t pt-40 mt-40"):
            price_labels = price_section.find_all("p", class_="s-text-subtle mb-0")
            for price_label in price_labels:
                label_text = price_label.get_text(strip=True).lower()
                if "pris" in label_text:
                    price_elem = price_section.find("span", class_="t2")
                    if price_elem:
                        data["price"] = price_elem.get_text(strip=True)
                    break
                elif "månadskostnad" in label_text:
                    monthly_elem = price_section.find("h2", class_="t2")
                    if monthly_elem:
                        data["monthly_cost"] = monthly_elem.get_text(strip=True)
                    break

    def _extract_description(self, grid: Tag, data: dict[str, Any]) -> None:
        desc_sections = grid.find_all("section", class_="border-t mt-40 pt-40")
        for section in desc_sections:
            h2 = section.find("h2", class_="t3 mb-0")
            if h2 and "beskrivning" in h2.get_text(strip=True).lower():
                desc_div = section.find("div", class_="whitespace-pre-wrap")
                if desc_div:
                    data["description"] = desc_div.get_text(strip=True)
                break

    def _extract_specifications(self, grid: Tag, data: dict[str, Any]) -> None:
        specs_section = grid.find("section", class_="key-info-section")
        if not specs_section:
            return

        dl = specs_section.find("dl")
        if not dl:
            return

        specifications: dict[str, str] = {}
        divs = dl.find_all("div", style="break-inside:avoid-column")
        for div in divs:
            dt = div.find("dt")
            dd = div.find("dd")
            if dt and dd:
                key_text = dt.get_text(strip=True)
                value_text = dd.get_text(strip=True)
                specifications[key_text] = value_text

        if specifications:
            data["specifications"] = specifications

    def _extract_equipment(self, grid: Tag, data: dict[str, Any]) -> None:
        equipment_section: Tag | None = None
        for section in grid.find_all("section", class_="border-t pt-40 mt-40"):
            h2 = section.find("h2", class_="t3 mb-0")
            if h2 and "utrustning" in h2.get_text(strip=True).lower():
                equipment_section = section
                break

        if not equipment_section:
            return

        equipment_list = equipment_section.find("ul")
        if equipment_list:
            equipment_items: list[str] = [
                li.get_text(strip=True) for li in equipment_list.find_all("li")
            ]
            if equipment_items:
                data["equipment"] = equipment_items

    def _extract_seller_type(self, soup: BeautifulSoup, data: dict[str, Any]) -> None:
        seller_type = (
            "dealer"
            if soup.find("div", class_=lambda x: x and "dealer" in str(x).lower())
            else "private"
        )
        data["seller_type"] = seller_type

    def _extract_ad_id(self, soup: BeautifulSoup, data: dict[str, Any]) -> None:
        ad_info_divs = soup.find_all(
            "div", class_="text-m flex md:flex-row flex-col md:gap-x-56 gap-y-16"
        )
        for div in ad_info_divs:
            ad_id_labels = div.find_all("p", class_="s-text-subtle mb-0")
            for ad_id_label in ad_id_labels:
                if "Annons-ID" in ad_id_label.get_text(strip=True):
                    ad_id_elem = ad_id_label.find_next_sibling("p")
                    if ad_id_elem:
                        data["ad_id"] = ad_id_elem.get_text(strip=True)
                        break
