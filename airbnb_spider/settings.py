# Scrapy settings for airbnb_spider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html
from airbnb_spider.lib.bbox import BBox
from airbnb_spider.lib.params import Params

LOG_LEVEL = 'INFO'
BOT_NAME = 'airbnb_spider'

# SPIDER_MODULES = ['airbnb_spider']
# NEWSPIDER_MODULE = 'airbnb_spider'

CONCURRENT_REQUESTS_PER_DOMAIN = 2
CONCURRENT_REQUESTS_PER_IP = 2
CONCURRENT_REQUESTS = 2

CONCURRENT_REQUESTS_PER_DOMAIN = 5
CONCURRENT_REQUESTS_PER_IP = 5
CONCURRENT_REQUESTS = 5
# DOWNLOAD_DELAY = 3
LOGSTATS_INTERVAL = 20
REQUEST_RESPONSE_DEBUG = False
REQUEST_RESPONSE_BODY_DEBUG = False

# FEED_EXPORT_BATCH_ITEM_COUNT = 100
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'airbnb_spider (+http://www.yourdomain.com)'
# FEEDS = {
#     "items.json": {"format": "jsonl"},
# }

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'airbnb_spider.middlewares.AirbnbSpiderSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'airbnb_spider.lib.middlewares.LoggingDownloaderMiddleware': 1000,
}
REQUEST_RESPONSE_DEBUG = False
REQUEST_RESPONSE_BODY_DEBUG = True
# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'airbnb_spider.lib.pipelines.ResultsDirPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = '2.7'
TWISTED_REACTOR = 'twisted.internet.asyncioreactor.AsyncioSelectorReactor'


PARAMS = Params(
    name="spain",
    start_date="2023-02-01", end_date="2023-02-07",
    # bbox=BBox(-7.710992,-21.093750,71.357067,157.148438) # all except USA, australia
    # bbox=BBox(39.7566663125, 30.4534576875, 39.844177875, 30.541219625),  # test
    bboxes_str="""http://bboxfinder.com/#35.889050,-11.469727,44.308127,5.097656"""
    # bbox=BBox(38.873929,39.396973,43.628123,50.866699) # georgia armenia azerbaijan
    # bbox=BBox(34.157095, 32.000526, 35.890134, 34.859832) # cyprus
)
