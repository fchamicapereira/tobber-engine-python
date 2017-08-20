import scrapy
import json

# Save all data in file
class Save(object):
    def open_spider(self, spider):
        self.first = True
        self.file = open(spider.file, 'w')
        self.file.write('{ "torrents": [\n')

    def close_spider(self, spider):
        self.file.write('\n] }')
        self.file.close()

    def process_item(self, item, spider):
        if self.first:
            line = json.dumps(dict(item))
            self.first = False
        else:
            line = ', \n' + json.dumps(dict(item))
        self.file.write(line)
        return item
