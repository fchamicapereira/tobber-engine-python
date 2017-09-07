import scrapy
from tobber.items import Torrent
from tobber.spiders.indexer import Indexer

class Limetorrents(Indexer):
    name = "limetorrents"

    def start_requests(self):
        print 'Limetorrents is scrapying...'

        self.site = "https://www.limetorrents.cc"
        urls = []
        search = self.site + "/search/all/"

        for title in self.title:
            urls.append(search + title.replace('%20','-') + '/')

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        table   = response.xpath('//table[@class="table2"]')
        row     = table.xpath('./tr')

        # content that matters starts at index 1
        for i in range(1, len(row)):

            title       = row[i].xpath('./td[@class="tdleft"]//div[@class="tt-name"]//a/text()')
            href        = row[i].xpath('./td[@class="tdleft"]//div[@class="tt-name"]//a/@href')[1]
            size        = row[i].xpath('./td[@class="tdnormal"]/text()')[1]
            seeders     = row[i].xpath('./td[@class="tdseed"]/text()')[0]
            leechers    = row[i].xpath('./td[@class="tdleech"]/text()')[0]
            torrent     = row[i].xpath('./td[@class="tdleft"]//div[@class="tt-name"]//a/@href')[0]

            yield Torrent(
                title       = self.extract_data(title),
                size        = size.extract(),
                seeders     = seeders.extract(),
                leechers    = leechers.extract(),
                href        = self.site + href.extract(),
                torrent     = torrent.extract(),
                site        = self.name,
                counter     = i
            )
