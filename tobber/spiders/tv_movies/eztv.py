import scrapy
from tobber.items import Torrent
from tobber.spiders.indexer import Indexer

class Eztv(Indexer):
    name = "EZTV"

    def start_requests(self):
        print 'EZTV is scrapying...'

        self.site = "https://eztv.ag"
        urls = []
        search = self.site + "/search/"

        for title in self.title:
            urls.append(search + title)

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        print 'Using User-Agent:',response.request.headers['User-Agent']

        # xPath rules
        table   = response.xpath('//table//tr[@class="forum_header_border"]')

        for row in range(len(table)):

            items = table[row].xpath('./td')

            title   = items[1].xpath('./a[@class="epinfo"]/text()').extract()[0].encode('ascii', 'ignore')
            href    = self.site + items[1].xpath('./a[@class="epinfo"]/@href').extract()[0].encode('ascii', 'ignore')
            seeders = items[5].xpath('./font/text()').extract()[0].encode('ascii', 'ignore')
            magnet  = items[2].xpath('./a[@class="magnet"]/@href').extract()[0].encode('ascii', 'ignore')
            torrent = items[2].xpath('./a[@class="download_1"]/@href').extract()[0].encode('ascii', 'ignore')
            size    = items[3].xpath('./text()').extract()[0].encode('ascii', 'ignore')

            yield Torrent(
                title       = title,
                magnet      = magnet,
                torrent     = torrent,
                size        = size,
                seeders     = seeders,
                href        = href,
                site        = self.name
            )
