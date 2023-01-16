import logging
from datetime import timedelta

import scrapy

# v.platformTrust = lambda: None
from airbnb_spider.lib.listing_request import ListingRequest
from airbnb_spider.lib.params import Params
from airbnb_spider.lib import utils

log = logging.getLogger(__name__)


class AirbnbSpider(scrapy.Spider):
    name = 'airbnb'

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        params = crawler.settings["PARAMS"]
        spider = cls(params=params, *args, **kwargs)
        spider._set_crawler(crawler)
        return spider

    def __init__(self, params: Params, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.params = params

    def start_requests(self):
        if self.params.bboxes_str:
            bboxes = utils.as_bboxes(self.params.bboxes_str)
        else:
            bboxes = [self.params.bbox]

        end_date = self.params.end_date or self.params.start_date + timedelta(days=self.params.days)
        for bbox in bboxes:
            log.info(f"Requesting {bbox}")
            for _start_date, _end_date in utils.dates_generator(start_date=self.params.start_date, end_date=end_date, step=self.params.days):
                yield ListingRequest(spider=self, bbox=bbox, start_date=_start_date, end_date=_end_date)
