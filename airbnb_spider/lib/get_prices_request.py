import json
import logging
import re
import sys

import attrs
import jsonpath_ng

from airbnb_spider.lib import utils
from airbnb_spider.lib.listing_request import ListingRequest
from airbnb_spider.lib.request import RequestBase

log = logging.getLogger(__name__)


@attrs.define(slots=False)
class Prices:
    min_price: int
    max_price: int

    def __str__(self):
        return f"Prices(min_price={self.min_price} max_price={self.max_price})"

    __repr__ = __str__


@attrs.define
class GetPricesRequest(RequestBase):

    def parse(self, response):
        items_count = self._get_items_count(response=response)
        if items_count == 0:
            log.debug(f"{self}: No items found")
            return

        prices = self._get_prices_range(response=response)
        min_price = max(prices.min_price, self.min_price or prices.min_price)
        max_price = min(prices.max_price, self.max_price or prices.max_price)
        log.debug(f"{self}: will scrape {items_count} items")
        log.debug(f"{self}: prices range: {prices}")
        if items_count > 600:
            for _min_price, _max_price in utils.gen_ranges(start=min_price, end=max_price, steps=10):
                new_request = attrs.evolve(self, min_price=_min_price, max_price=_max_price)
                yield new_request
        else:
            yield ListingRequest(spider=self, bbox=self.bbox, min_price=prices.min_price, max_price=prices.max_price,
                                 start_date=self.start_date, end_date=self.end_date)

    def _get_prices_range(self, response) -> Prices:
        expr = jsonpath_ng.parse(
            "$.data.presentation.explore.sections.sections[*].section.discreteFilterItems[*].[minValue,maxValue]")
        prices = Prices(*[item.value for item in expr.find(response.json())])
        return prices

    def _get_items_count(self, response):
        path = "$.data.presentation.explore.sections.sectionIndependentData.staysSearch.sectionConfiguration.pageTitleSections.sections[*].sectionData.structuredTitle"
        items = jsonpath_ng.parse(path).find(response.json())
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
