import scrapy

class Spider_init(scrapy.Spider):

    custom_settings = {
        "ITEM_PIPELINES": {
            'tobber.pipelines.print.Print': 970
        },

        "DOWNLOADER_MIDDLEWARES": {
            'tobber.middlewares.UserAgentMiddleware': 400,
            'tobber.middlewares.ProxyMiddleware': 410,
            'tobber.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None
        }
    }
