import json
from typing import Any, Dict

import attr
import attrs
import jsonpath_ng
import scrapy

from airbnb_spider.spiders import utils
from airbnb_spider.spiders.request import RequestBase, log


@attr.define
class ListingRequest(RequestBase):
    def parse(self, response: scrapy.http.Response):
        data = json.loads(response.text)

        expr = jsonpath_ng.parse(
            "$.data.presentation.explore.sections.sectionIndependentData.staysSearch.searchResults[*]")
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

    def __hash__(self):
        return id(self)

    def __str__(self):
        d = attr.asdict(self)
        next_page_cursor = d.pop("next_page_cursor")
        d["next_page_cursor"] = next_page_cursor[:5] + "..." if next_page_cursor else None
        d.pop("spider")
        # place = d.pop("place")
        # d["place"] = place.query
        d_str = " ".join(f"{k}={v}" for k, v in d.items() if v is not None)
        return f"{self.__class__.__name__}({d_str})"

    __repr__ = __str__
