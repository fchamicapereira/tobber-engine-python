import scrapy
import pymongo
from scrapy.exceptions import DropItem

# store in mongodb

class Mongo(object):

    def __init__(self, mongo_server, mongo_port, mongo_db, mongo_collection):
        self.mongo_server     = mongo_server
        self.mongo_port       = mongo_port
        self.mongo_db         = mongo_db
        self.mongo_collection = mongo_collection

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_server     = crawler.settings.get('MONGODB_SERVER'),
            mongo_port       = crawler.settings.get('MONGODB_PORT'),
            mongo_db         = crawler.settings.get('MONGODB_DB'),
            mongo_collection = crawler.settings.get('MONGODB_COLLECTION')
        )

    def open_spider(self, spider):

        try:
            self.client = pymongo.MongoClient(self.mongo_server, self.mongo_port, serverSelectionTimeoutMS=5)
            self.client.server_info()

        except pymongo.errors.ServerSelectionTimeoutError as err:
            print 'Mongo:', err
            raise scrapy.exceptions.CloseSpider('Can\'t connect to mongo database')

        self.db         = self.client[self.mongo_db]
        self.collection = self.db[self.mongo_collection]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):

        if 'magnet' not in item or self.collection.find_one({ "magnet": item['magnet'] }) == None:
            self.collection.insert_one(dict(item))
            return item

        raise DropItem('Torrent already added',search)
