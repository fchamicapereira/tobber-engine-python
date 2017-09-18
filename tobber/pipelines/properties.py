import scrapy

class Properties(object):

    def __init__(self):
        self.template = {
            'resolution': {
                '2160p':    ['uhd','4k','2160', '2160p', '3840x2160'],
                '1080p':    ['hd','1080', '1080p', '1920x1080'],
                '720p':     ['720', '720p', '1280x720'],
                '480p':     ['480', '480p']
            },

            'source': {
                'Remux':    ['remux'],
                'Bluray':   ['bluray','blu ray','bdrip','bd rip','brrip','br rip','bd'],
                'Web-dl':   ['webdl','web dl','web dl'],
                'Webrip':   ['webrip','web rip','web rip'],
                'HDTV':     ['hdtv'],
                'CAM':      ['cam'],
                "TS":       ['ts', 'hdts', 'hd ts'],
            },

            'audio': {
                'FLAC':     ['flac'],
                'AAC':      ['aac'],
                'DTS-HD':   ['dts hd', 'dts'],
                'DD':       ['dd 5 1', 'ac3', 'dd', 'dd5 1']
            },

            'encoding': {
                'HEVC':     ['x265','hevc','h265', 'h 265'],
                'h264':     ['x264','h264', 'h 264', 'avc'],
                'DivX':     ['divx'],
                'XviD':     ['xvid']
            },

            'group': {
                'PublicHD': ['publichd'],
                'SPARKS':   ['sparks'],
                'Yify':     ['yify'],
                'Grym':     ['grym'],
                'CtrlHD':   ['ctrlhd'],
                'Axxo':     ['axxo'],
                'VietHD':   ['viethd'],
                'TayTO':    ['tayto'],
                'EbP':      ['ebp'],
                'ESiR':     ['esir'],
                'DON':      ['don'],
                'NTb':      ['ntb'],
                'IDE':      ['ide'],
                'EA':       ['ea'],
                'HaB':      ['hab'],
                'CRiSC':    ['crisc'],
                'BMF':      ['bmf'],
                'SA89':     ['sa89'],
                'CRiME':    ['crime'],
                'RightSiZE':    ['rightsize'],
                'HorribleSubs': ['horriblesubs']
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
            if keys == 'title':
                self.searchKeywords(title,keys,properties)
            else:
                self.searchIsolated(title,keys,properties)

        return properties

    def searchKeywords(self,title,keys,properties):
        for subkeys in self.template[keys]:
            for word in self.template[keys][subkeys]:
                if word.lower() in title.lower():
                    properties[keys] = subkeys
                    return

    def searchIsolated(self,title,keys,properties):

        separators = ['%20', '_', '.', '-', '+', '(', ')', '[', ']']
        title = title.lower()

        for s in separators:
            title = title.replace(s,' ')

        title = title.split(' ')

        for subkeys in self.template[keys]:
            for word in self.template[keys][subkeys]:
                if word.lower() in title:
                    properties[keys] = subkeys
                    return
