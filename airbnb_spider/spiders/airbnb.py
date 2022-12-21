import logging
from itertools import tee

import scrapy
import numpy as np
from airbnb_spider.spiders import utils
from airbnb_spider.spiders.bbox import BBox
from airbnb_spider.spiders.place import Place
from airbnb_spider.spiders.get_prices_request import GetPricesRequest


# v.platformTrust = lambda: None
log = logging.getLogger(__name__)

def gen(start, end, steps):
    g1, g2 = tee(np.linspace(start, end, steps + 1, endpoint=True))
    next(g2)
    for start, end in zip(g1, g2):
        yield start, end

class AirbnbSpider(scrapy.Spider):
    name = 'airbnb'

    def start_requests(self):
        start_date = utils.to_date("2023-02-01")
        end_date = utils.to_date("2023-02-07")
        sw = (36.081554, 26.389847)
        ne = (41.765636, 44.437553)
        steps = 20
        for sw_lat, ne_lat in gen(sw[0], ne[0], steps=steps):
            for sw_lng, ne_lng in gen(sw[1], ne[1], steps=steps):
                bbox = BBox(sw_lat=sw_lat, sw_lng=sw_lng, ne_lat=ne_lat, ne_lng=ne_lng)
                log.info(f"Requesting {bbox=}")
                for _start_date, _end_date in utils.dates_generator(start_date=start_date, end_date=end_date):
                    yield GetPricesRequest(spider=self, bbox=bbox, start_date=_start_date, end_date=_end_date)
