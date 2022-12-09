import copy
import json
import logging
from datetime import date

import attrs
import scrapy

from airbnb_spider.spiders import utils, constants
from airbnb_spider.spiders.filters import Filters
from airbnb_spider.spiders.middlewares import request_httprepr, response_httprepr
from airbnb_spider.spiders.place import Place

log = logging.getLogger(__name__)


@attrs.define
class RequestBase(scrapy.Request):
    spider: scrapy.Spider
    place: Place
    start_date: date
    end_date: date
    min_price: int = None
    max_price: int = None
    next_page_cursor: str = None

    def __hash__(self):
        return id(self)

    def __attrs_post_init__(self):
        log.debug(f'Requesting page:{self.next_page_cursor} {self.min_price=} {self.max_price=} '
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

        super().__init__(url=constants.STAY_SEARCH_URL, method="POST", headers=constants.headers.items(), body=json.dumps(data),
                         callback=self.parse, errback=self.errback)

    def parse(self, response):
        raise NotImplementedError

    def errback(self, failure):
        # if failure.check(HttpError) and "Session expired (invalid CSRF token)" in failure.value.response.text:
        #     log.info("Session expired, restarting")
        #     return self._create_session_request(cookiejar=failure.value.response.meta["cookiejar"])

        log.info(failure)
        log.info("Request:\n" + request_httprepr(failure.request))
        if response := getattr(failure.value, "response", None):
            log.info("Reponse:\n" + response_httprepr(failure.value.response))
        else:
            log.info("No reponseReponse:\n" + response_httprepr(failure.value.response))
