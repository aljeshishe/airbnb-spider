import os

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from airbnb_spider.lib import airbnb_spider


def run_spider():
    os.environ["SCRAPY_SETTINGS_MODULE"] = "airbnb_spider.settings"
    process = CrawlerProcess(settings=get_project_settings())
    process.crawl(airbnb_spider.AirbnbSpider)
    process.start()



if __name__ == "__main__":
    run_spider()
