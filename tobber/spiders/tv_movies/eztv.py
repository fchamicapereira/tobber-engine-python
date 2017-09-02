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

        # xPath rules
        table   = response.xpath('//table//tr[@class="forum_header_border"]')

        for i in range(len(table)):
            items = table[i].xpath('./td')

            title   = self.extract_data(items[1].xpath('./a[@class="epinfo"]/text()'))
            href    = self.site + self.extract_data(items[1].xpath('./a[@class="epinfo"]/@href'))
            seeders = self.extract_data(items[5].xpath('./font/text()'))
            magnet  = self.extract_data(items[2].xpath('./a[@class="magnet"]/@href'))
            torrent = self.extract_data(items[2].xpath('./a[@class="download_1"]/@href'))
            size    = self.extract_data(items[3].xpath('./text()'))

            yield Torrent(
                title       = title,
                magnet      = magnet,
                torrent     = torrent,
                size        = size,
                seeders     = seeders,
                href        = href,
                site        = self.name,
                counter     = i
            )
