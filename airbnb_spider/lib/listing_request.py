import json
import re
from typing import Any, Dict

import attr
import attrs
import jsonpath_ng
import scrapy

from airbnb_spider.lib import utils
from airbnb_spider.lib.bbox import BBox
from airbnb_spider.lib.request import RequestBase, log


@attr.define
class ListingRequest(RequestBase):
    def parse(self, response: scrapy.http.Response):
        data = response.json()

        expected_items_count = self._get_items_count(data=data)
        log.info(f"{self}: {expected_items_count=}")
        if expected_items_count == 0:
            log.debug(f"{self}: No items found")
            return
        if expected_items_count > 600:
            steps = 4
            for sw_lat, ne_lat in utils.gen_ranges(self.bbox.sw_lat, self.bbox.ne_lat, steps=steps):
                for sw_lng, ne_lng in utils.gen_ranges(self.bbox.sw_lng, self.bbox.ne_lng, steps=steps):
                    bbox = BBox(sw_lat=sw_lat, sw_lng=sw_lng, ne_lat=ne_lat, ne_lng=ne_lng)
                    log.info(f"Requesting {bbox=}")
                    new_request = attrs.evolve(self, bbox=bbox)
                    yield new_request
            return

        expr = jsonpath_ng.parse("$.data.presentation.explore.sections.sectionIndependentData.staysSearch.searchResults[*]")
        items = expr.find(data)
        log.info(f"{self}: Got {len(items)} items")
        for item in items:
            item = utils.normalize(d=item.value)
            item.update(dict(start_date=self.start_date, end_date=self.end_date, min_price=self.min_price,
                             max_price=self.max_price))
            item = self._prepare_item(item=item)
            yield item

        next_page_cursor = self._get_next_page_cursor(data=data)
        if next_page_cursor is None:
            return
        new_request = attrs.evolve(self, next_page_cursor=next_page_cursor)
        yield new_request

    def _get_next_page_cursor(self, data: dict[str, Any]) -> str:
        expr = jsonpath_ng.parse(
            "data.presentation.explore.sections.sectionIndependentData.staysSearch.paginationInfo.nextPageCursor")
        next_page_cursors = expr.find(data)
        assert len(next_page_cursors) == 1
        return next_page_cursors[0].value

    def _prepare_item(self, item: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        item["place_name"] = self.place.query if self.place is not None else ""
        item.update(kwargs)
        return item

    def _get_items_count(self, data):
        path = "$.data.presentation.explore.sections.sectionIndependentData.staysSearch.sectionConfiguration.pageTitleSections.sections[*].sectionData.structuredTitle"
        items = jsonpath_ng.parse(path).find(data)
        if not items:
            return 0

        if "over" in items[0].value.lower():
            return 1001

        assert len(items) == 1, f"Expected 1 item, got {len(items)}"
        result = re.match(r"(\d+) homes", items[0].value)
        assert result is not None, f"Cant parse {items[0].value}"
        return int(result.group(1))

    def __hash__(self):
        return id(self)

