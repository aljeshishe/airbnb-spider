import json
import logging

import attrs
import jsonpath_ng

from airbnb_spider.spiders import utils
from airbnb_spider.spiders.listing_request import ListingRequest
from airbnb_spider.spiders.request import RequestBase

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
        prices = self._get_prices_range(response=response)
        for _min_price, _max_price in utils.iterate_prices(start=prices.min_price, end=prices.max_price, step=5):
            yield ListingRequest(spider=self, bbox=self.bbox, min_price=_min_price, max_price=_max_price,
                                 start_date=self.start_date, end_date=self.end_date)

    def _get_prices_range(self, response) -> Prices:
        expr = jsonpath_ng.parse(
            "$.data.presentation.explore.sections.sections[*].section.discreteFilterItems[*].[minValue,maxValue]")
        prices = Prices(*[item.value for item in expr.find(json.loads(response.text))])
        log.info(f"{prices}")
        return prices

    def __hash__(self):
        return id(self)
