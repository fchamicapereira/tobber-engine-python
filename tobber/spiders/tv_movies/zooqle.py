import scrapy
from tobber.items import Torrent
from tobber.spiders.indexer import Indexer

class Zooqle(Indexer):
    name = "zooqle"

    def start_requests(self):
        print 'Zooqle is scrapying...'

        self.site = "https://zooqle.com"
        urls = []
        sortBySize = "&s=sz&v=t&sd=d"
        search = self.site + "/search?q="

        for title in self.title:
            urls.append(search + title)

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        #xPath rules
        table   = response.xpath('//table[contains(@class,"table-torrents")]')
        row     = table.xpath('./tr')

        for i in range(len(row)):

            data = row[i].xpath('./td')
            href = data[1].xpath('./a/@href')

            # this is a hack
            # the title's text comes with <hl> tags that are
            # troublessome, so this will remove all the
            # garbage
            title   = data[1].xpath('./a')
            title   = title[0].extract().split('>',1)[1][:-4]
            title   = title.replace('<hl>','').replace('</hl>','')

            links   = data[2].xpath('./ul//li')
            magnet  = links[1].xpath('./a/@href')
            torrent = links[2].xpath('./a/@href')

            size    = data[3].xpath('./div//div/text()')

            peers   = data[5].xpath('./div/@title')

            # Seeders : X | Leechers: Y
            peersTuple = peers.re(r'(\d+).* (\d+)')

            seeders  = peersTuple[0]
            leechers = peersTuple[1]

            yield Torrent(
            title       = title,
            magnet      = self.extract_data(magnet),
            href        = self.site + self.extract_data(href),
            torrent     = self.site + self.extract_data(torrent),
            size        = self.extract_data(size),
            seeders     = seeders,
            leechers    = leechers,
            site        = self.name,
            counter     = i
            )
