import scrapy
from tobber.items import Torrent
from tobber.spiders.indexer import Indexer

class Thepiratebay(Indexer):
    name = "thepiratebay"

    def start_requests(self):
        print 'ThePirateBay is scrapying...'

        self.site = "https://thebay.tv"
        urls = []
        page = "&page=0"
        sort = "&orderby=99"
        search = self.site + "/s/?q="

        for title in self.title:
            urls.append(search + title.replace('%20','+') + page + sort)

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        #xPath rules
        table   = response.xpath('//table[@id="searchResult"]')
        row     = table.xpath('./tr')

        for i in range(len(row)):

            data    = row[i].xpath('./td')
            href    = data[1].xpath('./div[@class="detName"]//@href')

            title   = data[1].xpath('./div[@class="detName"]//a/text()')

            # size is in the middle of this string, gotta extract it
            size    = data[1].xpath('./font/text()').extract()[0]
            size    = size.split(', ')[1].split('Size ')[1].replace(u'\xa0',' ').encode('ascii','ignore')

            seeders     = data[2].xpath('./text()')
            leechers    = data[3].xpath('./text()')

            yield Torrent(
            title       = self.extract_data(title),
            href        = self.site + self.extract_data(href),
            size        = size,
            seeders     = self.extract_data(seeders),
            leechers    = self.extract_data(leechers),
            site        = self.name,
            counter     = i
            )
