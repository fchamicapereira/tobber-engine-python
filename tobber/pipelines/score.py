import scrapy
import json
import math
import pymongo

class Score(object):

    def __init__(self, score_rules, rules_mongo, mongo_server, mongo_port, mongo_db):
        if len(rules_mongo) == 0:
            self.load_rules_from_file(score_rules)

        else:
            rules = rules_mongo.split('/')

            mongo_server       = mongo_server
            mongo_port         = mongo_port
            mongo_db           = mongo_db
            mongo_collection   = rules[0]
            mongo_document     = rules[1]

            try:
                client = pymongo.MongoClient(mongo_server, mongo_port, serverSelectionTimeoutMS=5)
                client.server_info()

            except pymongo.errors.ServerSelectionTimeoutError as err:
                print 'Mongo:', err
                raise scrapy.exceptions.CloseSpider('Can\'t connect to mongo database')

            db = client[mongo_db]
            collection = db[mongo_collection]

            user = collection.find_one({"name": mongo_document})

            if 'rules' in user:
                self.rules = user["rules"]
            else:
                self.load_rules_from_file(score_rules)

            client.close()

    def load_rules_from_file(self, score_rules):
        with open(score_rules) as score_rules:
            self.rules = json.load(score_rules)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            score_rules     = crawler.settings.get('SCORE_RULES'),
            rules_mongo     = crawler.settings.get('RULES_MONGO'),
            mongo_server    = crawler.settings.get('MONGODB_SERVER'),
            mongo_port      = crawler.settings.get('MONGODB_PORT'),
            mongo_db        = crawler.settings.get('MONGODB_DB')
        )

    def process_item(self, item, spider):

        # get size in bytes and log_10 it
        score = self.getSizeBytes(item['size'])
        properties = item['properties']

        for key in self.rules:
            if key in properties:
                score *= self.rules[key][properties[key]]

        item['score'] = math.log(score)

        return item

    def getSizeBytes(self,size):

        # '12.2 Gib' -> ['12.2','Gib']
        size = size.split(' ')

        # get size number
        sizeBytes = float(size[0].replace(',',''))

        if 'G' in size[1]:
            sizeBytes *= 1e9

        elif 'M' in size[1]:
            sizeBytes *= 1e6

        elif 'K' in size[1]:
            sizeBytes *= 1e3

        return sizeBytes
