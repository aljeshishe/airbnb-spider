import copy
import dataclasses
import json
import logging
from datetime import date
from typing import Any, Dict

import jsonpath_ng
import scrapy

from airbnb_spider.spiders import utils, constants
from airbnb_spider.spiders.filters import Filters
from airbnb_spider.spiders.place import Place

log = logging.getLogger(__name__)


@dataclasses.dataclass
class Request(scrapy.Request):
    spider: scrapy.Spider
    place: Place
    start_date: date
    end_date: date
    min_price: int = None
    max_price: int = None
    next_page_cursor: str = None

    def __post_init__(self):
        log.info(f'Requesting page:{self.next_page_cursor} {self.min_price=} {self.max_price=} '
                 f'start_date={utils.from_date(self.start_date)} end_date={utils.from_date(self.end_date)}')

        data = copy.deepcopy(constants.STAY_SEARCH_DATA_2)
        data["variables"]["staysSearchRequest"]["cursor"] = self.next_page_cursor
        filters = Filters(data["variables"]["staysSearchRequest"]["rawParams"])
        filters["placeId"] = self.place.id
        filters["itemsPerGrid"] = constants.items_per_page
        if self.min_price is not None:
            filters["priceMin"] = self.min_price
        if self.min_price is not None:
            filters["priceMax"] = self.max_price
        if self.start_date is not None:
            filters["checkin"] = utils.from_date(self.start_date)
        if self.end_date is not None:
            filters["checkout"] = utils.from_date(self.end_date)
        if self.start_date is not None and self.end_date is not None:
            filters["priceFilterNumNights"] = (self.end_date - self.start_date).days

        super().__init__(url=constants.STAY_SEARCH_URL, method="POST", headers=constants.headers, body=json.dumps(data),
                         callback=self.parse)

    def parse(self, response):
        data = json.loads(response.text)

        expr = jsonpath_ng.parse(
            "$.data.presentation.explore.sections.sectionIndependentData.staysSearch.searchResults[*]")
        items = expr.find(response.text)
        log.info(f"Got {len(items)} items")
        for item in items:
            item = utils.normalize(d=item.value)
            item.update(dict(start_date=self.start_date, end_date=self.end_date, min_price=self.min_price,
                             max_price=self.max_price))
            item = self._prepare_item(item=item)
            yield item

        next_page_cursor = self._get_next_page_cursor(data=data)
        if next_page_cursor is None:
            return
        new_request = dataclasses.replace(self, next_page_cursor=next_page_cursor)
        yield new_request

    def _get_next_page_cursor(self, data: dict[str, Any]) -> str:
        expr = jsonpath_ng.parse(
            "data.presentation.explore.sections.sectionIndependentData.staysSearch.paginationInfo.nextPageCursor")
        next_page_cursors = expr.find(data)
        assert len(next_page_cursors) == 1
        return next_page_cursors[0].value

    def _prepare_item(self, item: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        item["place_name"] = self.place.query
        item.update(kwargs)
        return item
