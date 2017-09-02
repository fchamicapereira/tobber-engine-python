# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import json

class Torrent(scrapy.Item):
    title       = scrapy.Field()
    magnet      = scrapy.Field()
    torrent     = scrapy.Field()
    size        = scrapy.Field()
    category    = scrapy.Field()
    href        = scrapy.Field()
    seeders     = scrapy.Field()
    leechers    = scrapy.Field()
    properties  = scrapy.Field()
    score       = scrapy.Field()
    site        = scrapy.Field()
    counter     = scrapy.Field()
