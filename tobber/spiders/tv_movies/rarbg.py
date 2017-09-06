import scrapy
from tobber.items import Torrent
from tobber.spiders.indexer import Indexer

class Rarbg(Indexer):
    name = "rarbg"

    def start_requests(self):
        print 'Rarbg is scrapying...'

        self.site = "https://rarbg.is"
        urls = []
        search = self.site + "/torrents.php?search="

        for title in self.title:
            urls.append(search + title.replace('%20','+'))

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        #xPath rules
        table   = response.xpath('//table[@class="lista2t"]')
        row     = table.xpath('./tr[@class="lista2"]')


        for i in range(len(row)):

            content = row[i].xpath('./td[@class="lista"]')

            title       = content[1].xpath('./a/@title')
            href        = content[1].xpath('./a/@href')
            size        = content[3].xpath('./text()')
            seeders     = content[4].xpath('./font/text()')
            leechers    = content[5].xpath('./text()')

            yield Torrent(
                title       = self.extract_data(title),
                size        = self.extract_data(size),
                seeders     = self.extract_data(seeders),
                leechers    = self.extract_data(leechers),
                href        = self.extract_data(href),
                site        = self.name,
                counter     = i
            )
