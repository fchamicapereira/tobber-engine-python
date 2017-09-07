import scrapy
from tobber.items import Torrent
from tobber.spiders.indexer import Indexer

class Torrentdownloads(Indexer):
    name = "torrentdownloads"

    def start_requests(self):
        print 'Torrentdownloads is scrapying...'

        self.site = "https://www.torrentdownloads.me"
        urls = []
        search = self.site + "/search/?search="

        for title in self.title:
            urls.append(search + title.replace('%20','+'))

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        #xPath rules
        table   = response.xpath('//div[@class="inner_container"]')
        row     = table[1].xpath('./div[contains(@class,"grey_bar3")]')

        # content that matters starts at index 3
        for i in range(2, len(row) - 1):

            title       = row[i].xpath('./p//a/@title')
            href        = row[i].xpath('./p//a/@href')
            size        = row[i].xpath('./span/text()')[2]
            seeders     = row[i].xpath('./span/text()')[1]
            leechers    = row[i].xpath('./span/text()')[0]

            yield Torrent(
                title       = self.extract_data(title).split('View torrent info : ')[1],
                size        = size.extract().replace(u'\xa0', u' '),
                seeders     = seeders.extract(),
                leechers    = leechers.extract(),
                href        = self.site + self.extract_data(href),
                site        = self.name,
                counter     = i
            )
