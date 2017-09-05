import scrapy

class Properties(object):

    def __init__(self):
        self.template = {
            'resolution': {
                '2160p':    ['uhd','4k','2160'],
                '1080p':    ['hd','1080'],
                '720p':     ['720'],
                '480p':     ['480']
            },

            'source': {
                'Remux':    ['remux'],
                'Bluray':   ['bluray','blu-ray','bdrip','bd-rip','brrip','br rip','br-rip','bd'],
                'Web-dl':   ['webdl','web-dl','web dl'],
                'Webrip':   ['webrip','web-rip','web rip'],
                'HDTV':     ['hdtv'],
                'CAM':      ['cam']
            },

            'audio': {
                'FLAC':     ['flac'],
                'AAC':      ['aac']
            },

            'encoding': {
                'HEVC':     ['x265','hevc','h265'],
                'h264':     ['x264','h264'],
                'DivX':     ['divx'],
                'XviD':     ['xvid']
            },

            'format': {
                'mkv':      ['mkv'],
                'mp4':      ['mp4']
            }
        }

    def process_item(self, item, spider):
        item['properties'] = self.getProperties(item['title'])
        return item


    def getProperties(self,title):
        properties = {}

        for keys in self.template:
            self.searchKeywords(title,keys,properties)

        return properties

    def searchKeywords(self,title,keys,properties):
        for subkeys in self.template[keys]:
            for word in self.template[keys][subkeys]:
                if word.lower() in title.lower():
                    properties[keys] = subkeys
                    return
