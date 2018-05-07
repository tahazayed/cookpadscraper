# -*- coding: utf-8 -*-

# Scrapy settings for cookpad project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'cookpad'

SPIDER_MODULES = ['cookpad.spiders']
NEWSPIDER_MODULE = 'cookpad.spiders'
LOG_LEVEL = 'ERROR'
LOG_FILE = 'cookpad.log'


IS_MSSQLDB = True

ITEM_PIPELINES = {'cookpad.pipelines.MongoDBPipeline':300}

MONGODB_SERVER = "ds127321.mlab.com"
MONGODB_PORT = 27321
MONGODB_DB = "heroku_v65c6f57"
MONGODB_COLLECTION_RECIPES = "recipes"
MONGODB_COLLECTION_RECIPES_SPIDER = 'recipes_spider'
MONGODB_USER = "admin"
MONGODB_PASSWORD = "dodido_2008"

MSSQL_SERVER = "."
MSSQL_DB = "meals"
MSSQL_USER = "meals"
MSSQL_PASSWORD = "dodido_2008"

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'cookpad (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False
DOWNLOADER_MIDDLEWARES = {
            'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': 300}

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 100

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 0
# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 100
CONCURRENT_REQUESTS_PER_IP = 100

# Disable cookies (enabled by default)
COOKIES_ENABLED = True
COOKIES_DEBUG = False
# Disable Telnet Console (enabled by default)
TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Referer': 'https://cookpad.com/eg/%D9%88%D8%B5%D9%81%D8%A7%D8%AA',
    'Turbolinks-Referrer': 'https://cookpad.com/eg/%D9%88%D8%B5%D9%81%D8%A7%D8%AA',
    'X-Turbolinks-Request': 'true',
    'Accept': 'text/html, application/xhtml+xml',
    'Accept-Encoding': 'gzip, deflate, sdch, br',
    'Accept-Language': 'en-US,en;q=0.8,ar;q=0.6'
}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'cookpad.middlewares.CookpadSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'cookpad.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'cookpad.pipelines.CookpadPipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = False
# The initial download delay
AUTOTHROTTLE_START_DELAY = 0
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 3
# The average number of requests Scrapy should be sending in parallel to
# each remote server
AUTOTHROTTLE_TARGET_CONCURRENCY = 16.0
# Enable showing throttling stats for every response received:
AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
HTTPCACHE_ENABLED = False
HTTPCACHE_EXPIRATION_SECS = 0
HTTPCACHE_DIR = './httpcache'
HTTPCACHE_IGNORE_HTTP_CODES = [502]
HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
HTTPCACHE_GZIP = True
