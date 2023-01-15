from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from airbnb_spider.spiders.airbnb import AirbnbSpider


def run_spider():
    process = CrawlerProcess(settings=get_project_settings())
    process.crawl(AirbnbSpider, params=AirbnbSpider.DEFAULT_PARAMS)
    process.start()


if __name__ == "__main__":
    run_spider()
