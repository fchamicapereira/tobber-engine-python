import scrapy
import json
import math

class Score(object):

    def __init__(self, score_rules):
        with open(score_rules) as score_rules:
            self.rules = json.load(score_rules)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            score_rules = crawler.settings.get('SCORE_RULES'),
        )

    def process_item(self, item, spider):

        # get size in bytes and log_10 it
        score = math.log(self.getSizeBytes(item['size']))
        properties = item['properties']

        for key in self.rules:
            if key in properties:
                score *= self.rules[key][properties[key]]

        item['score'] = score

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
