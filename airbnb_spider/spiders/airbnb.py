import logging

import attr
import scrapy

from airbnb_spider.spiders import utils
from airbnb_spider.spiders.bbox import BBox
# v.platformTrust = lambda: None
from airbnb_spider.spiders.listing_request import ListingRequest

log = logging.getLogger(__name__)


@attr.define
class Params:
    start_date: str = attr.field(converter=utils.to_date)
    end_date: str = attr.field(converter=utils.to_date)
    bbox: BBox


class AirbnbSpider(scrapy.Spider):
    DEFAULT_PARAMS = Params(start_date="2023-02-01", end_date="2023-02-07",
                            # bbox=BBox(-7.710992,-21.093750,71.357067,157.148438) # all except USA, australia
                            bbox=BBox(38.873929,39.396973,43.628123,50.866699) # georgia armenia azerbaijan
                            # bbox=BBox(34.157095, 32.000526, 35.890134, 34.859832) # cyprus
                            )
    name = 'airbnb'

    def __init__(self, params: Params, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.params = params

    def start_requests(self):
        log.info(f"Requesting {self.params.bbox}")

        for _start_date, _end_date in utils.dates_generator(start_date=self.params.start_date,
                                                            end_date=self.params.end_date):
            yield ListingRequest(spider=self, bbox=self.params.bbox, start_date=_start_date, end_date=_end_date)
