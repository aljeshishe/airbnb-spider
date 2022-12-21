import logging
import sys

import scrapy
from airbnb_spider.spiders import utils
from airbnb_spider.spiders.bbox import BBox
from airbnb_spider.spiders.get_prices_request import GetPricesRequest


# v.platformTrust = lambda: None
from airbnb_spider.spiders.utils import gen_ranges

log = logging.getLogger(__name__)


class AirbnbSpider(scrapy.Spider):
    name = 'airbnb'

    def start_requests(self):
        start_date = utils.to_date("2023-02-01")
        end_date = utils.to_date("2023-02-07")
        sw = (36.081554, 26.389847)
        ne = (41.765636, 44.437553)
        steps = 100
        for sw_lat, ne_lat in gen_ranges(sw[0], ne[0], steps=steps):
            for sw_lng, ne_lng in gen_ranges(sw[1], ne[1], steps=steps):
                bbox = BBox(sw_lat=sw_lat, sw_lng=sw_lng, ne_lat=ne_lat, ne_lng=ne_lng)
                log.info(f"Requesting {bbox=}\nhttps://www.google.com/maps/search/{sw_lat},{sw_lng}\nhttps://www.google.com/maps/search/{ne_lat},{ne_lng}")

                for _start_date, _end_date in utils.dates_generator(start_date=start_date, end_date=end_date):
                    yield GetPricesRequest(spider=self, bbox=bbox, start_date=_start_date, end_date=_end_date)
