import logging

import scrapy
import twisted.internet._sslverify as v

from airbnb_spider.spiders import utils
from airbnb_spider.spiders.place import Place
from airbnb_spider.spiders.get_prices_request import GetPricesRequest


# v.platformTrust = lambda: None
# log = logging.getLogger(__name__)


class AirbnbSpider(scrapy.Spider):
    name = 'airbnb'

    def start_requests(self):
        # cities = """
        # Kas,turkey
        # Antalya,turkey
        # Alanya,turkey
        # Istanbul,turkey
        # Bagcilar,turkey
        # Kucukcekmece,turkey
        # Batumi,georgia
        # Tbilisi,georgia
        # """
        cities = """
        Kucukcekmece,turkey
        """

        start_date = utils.to_date("2023-02-01")
        end_date = utils.to_date("2023-02-7")
        for query in cities.strip().split():
            place = Place.from_query(query=query.strip())
            for _start_date, _end_date in utils.dates_generator(start_date=start_date, end_date=end_date):
                yield GetPricesRequest(spider=self, place=place, start_date=_start_date, end_date=_end_date)
