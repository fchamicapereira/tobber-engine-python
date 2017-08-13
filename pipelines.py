# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
import json

# Gives score to torrents according to my tastes

class GetScore(object):

    def process_item(self, item, spider):
        return item

class PrintItem(object):
    def process_item(self, item, spider):
        print item

# Save all data in file
class ExportJson(object):
    def open_spider(self, spider):
        self.file = open('torrents.jl', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item

# Dump raw anime
class GetEnglishAnime(object):
    def process_item(self, item, spider):
        avoid = [
            'non',
            'raw',
            'audio'
        ]

        # only anime torrents have a category
        if 'category' in item and all(words not in item['category'].lower() for words in avoid):
            return item

        raise DropItem('Only english translated anime is desirable')
