import scrapy
from tobber.items import Torrent
from tobber.spiders.indexer import Indexer

class Nyaa(Indexer):
    name = "nyaa"

    def start_requests(self):
        print 'Nyaa is scrapying...'

        self.site = "https://nyaa.pantsu.cat"
        urls = []

        for title in self.title:
            urls.append(self.site + "/search?c=_&order=false&q=" + title + '&sort=4&userID=0')

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        #xPath rules
        table   = response.xpath('//tbody[@id="torrentListResults"]//tr[contains(@class,"torrent-info")]')
        title   = table.xpath('//td[@class="tr-name home-td"]//a/text()')
        category   = table.xpath('//td[@class="tr-cat home-td"]//div//a/@title')
        #href    = title.xpath('//td//@href')
        links   = table.xpath('//td[contains(@class,"tr-links home-td")]')
        magnet  = links.xpath('//a[@title="Magnet Link"]/@href')
        torrent = links.xpath('//a[@title="Torrent file"]/@href')
        size    = table.xpath('//td[contains(@class,"tr-size")]/text()')

        for i in range(len(table)):

            yield Torrent(
                title       = title[i].extract().replace('\n',''),
                magnet      = magnet[i].extract().encode('ascii','ignore'),
                torrent     = torrent[i].extract().encode('ascii','ignore'),
                size        = size[i].extract().replace('\n','').encode('ascii','ignore'),
                category    = category[i].extract().replace('\n','').encode('ascii','ignore'),
                site        = self.name,
                counter     = i
            )
