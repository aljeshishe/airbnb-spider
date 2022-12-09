import copy
import logging
from datetime import date
from typing import Any

import jsonpath_ng
import requests
import scrapy
import treq
import twisted.internet._sslverify as v
from scrapy.utils.defer import deferred_to_future

from airbnb_spider.spiders import constants, utils
from airbnb_spider.spiders.filters import Filters
from airbnb_spider.spiders.place2 import Place, iterate_prices
from airbnb_spider.spiders.request import Request

v.platformTrust = lambda: None
log = logging.getLogger(__name__)


class AirbnbSpider(scrapy.Spider):
    name = 'airbnb'

    def start_requests(self):
        cities = """
        Kas,turkey
        Antalya,turkey
        Alanya,turkey
        Istanbul,turkey
        Bagcilar,turkey
        Kucukcekmece,turkey
        Batumi,georgia
        Tbilisi,georgia
        """

        start_date = utils.to_date("2022-12-01")
        end_date = utils.to_date("2023-12-01")
        for query in cities.strip().split():
            place = Place.from_query(query=query.strip())
            for _start_date, _end_date in utils.dates_generator(start_date=start_date, end_date=end_date):
                prices = self._get_prices_range(start_date=start_date, end_date=end_date)
                for _min_price, _max_price in iterate_prices(*prices, step=5):
                    yield Request(spider=self, place=place, min_price=_min_price, max_price=_max_price,
                                  start_date=_start_date, end_date=_end_date)

    def _get_prices_range(self, start_date: date, end_date: date):
        data = self._request(start_date=start_date, end_date=end_date)
        expr = jsonpath_ng.parse("$.data.presentation.explore.sections.sections[*].section.discreteFilterItems[*].[minValue,maxValue]")
        prices = [item.value for item in expr.find(data)]
        assert len(prices) == 2
        log.info(f"Prices range: [{prices[0]}-{prices[1]}]")
        return prices

