import scrapy

class Zooqle(scrapy.Spider):
    name = "zooqle"

    def start_requests(self):
        self.site = "https://zooqle.com"

        tvshow = "rick and morty"
        sortBySize = "&s=sz&v=t&sd=d"

        search = self.site + "/search?q=" + tvshow.replace(' ','%20') + sortBySize

        #must return an iterable
        #can be a list (like here) or a generator (use yield in that case)
        return [scrapy.Request(url=search, callback=self.parse)]

    # pretty printing
    def printTorrent(self,torrent):
        print '\n{'
        print '\t Title: ' + torrent['title']
        print '\t Torrent: ' + torrent['torrent']
        print '\t Magnet: ' + torrent['magnet']
        print '\t Size: ' + torrent['size']
        print '\t Seeders: ' + str(torrent['seeders'])
        print '\t Leechers: ' + str(torrent['leechers'])
        print '}\n'

    def parse(self, response):
        table = response.xpath('//table//tr//td')

        title   = table.xpath('//a[@class=" small"]')
        peers   = table.xpath('//div[@class="progress prog trans70"]/@title')
        magnet  = table.xpath('//a[@title="Magnet link"]/@href')
        torrent = table.xpath('//a[@title="Generate .torrent"]/@href')
        size    = table.xpath('//div[@class="progress prog prog-narrow trans90"]//div[@class="progress-bar prog-blue prog-l"]/text()')

        for i in range(0,20):

            # peers' items come in format 'Seeders: X | Leechers: Y'
            # this is extract the numbers from that string

            peersList = [int(d) for d in peers[i].extract().split() if d.isdigit()]

            # this is a hack
            # the title's text comes with <hl> tags that are
            # troublessome, so this will remove all the
            # garbage

            t = title[i].extract().split('>',1)[1][:-4]
            t = t.replace('<hl>','')
            t = t.replace('</hl>','')

            obj = {
                'magnet': magnet[i].extract(),
                'torrent': self.site + torrent[i].extract(),
                'seeders': peersList[0],
                'leechers': peersList[1],
                'size': size[i].extract(),
                'title': t
            }

            self.printTorrent(obj)

            yield obj
