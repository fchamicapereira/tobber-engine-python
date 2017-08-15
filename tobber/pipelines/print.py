import scrapy
import json

class Print(object):

    def process_item(self, item, spider):
        print ''
        print 'Title:      ' + item['title']
        print 'Size:       ' + item['size']
        print 'Category:   ' + item['category']
        print 'Properties: ' + json.dumps(item['properties'],indent=4, sort_keys=True) + '\n'
        print 'Score:      ' + str(item['score'])
        return item
