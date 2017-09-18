import scrapy
import json

class Properties(object):

    def __init__(self, score_rules):
        with open(score_rules) as score_rules:
            self.score_rules = json.load(score_rules)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            score_rules = crawler.settings.get('SCORE_RULES'),
        )

    def process_item(self, item, spider):
        item['properties'] = self.getProperties(item['title'])
        return item


    def getProperties(self,title):
        properties = {}

        for keys in self.score_rules:
            self.searchIsolated(title,keys,properties)

        return properties

    def searchIsolated(self,title,keys,properties):

        separators = ['%20', '_', '.', '-', '+', '(', ')', '[', ']']
        title = title.lower()

        for s in separators:
            title = title.replace(s,' ')

        for subkeys in self.score_rules[keys]:
            for word in self.score_rules[keys][subkeys]["keywords"]:

                if word.lower() in title:
                    properties[keys] = subkeys
                    return
