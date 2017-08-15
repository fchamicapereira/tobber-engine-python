import scrapy
import json

class Score(object):

    # import rules
    def __init__(self):
        with open('score_rules.json') as score_rules:
            self.rules = json.load(score_rules)

    def process_item(self, item, spider):

        # get size in bytes
        score = self.getSizeBytes(item['size'])

        

        item['score'] = score

        return item

    def getSizeBytes(self,size):

        # '12.2 Gib' -> ['12.2','Gib']
        size = size.split(' ')

        # get size number
        sizeBytes = float(size[0])

        if 'G' in size[1]:
            sizeBytes *= 1e9

        elif 'M' in size[1]:
            sizeBytes *= 1e6

        elif 'K' in size[1]:
            sizeBytes *= 1e3

        return sizeBytes
