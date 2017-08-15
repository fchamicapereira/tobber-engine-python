import scrapy
from tobber.items import Torrent

class Nyaa(scrapy.Spider):
    name = "nyaa"

    def start_requests(self):
        self.site = "https://nyaa.pantsu.cat"

        tvshow = "steins;gate"
        search = self.site + "/search?c=_&order=false&q=" + tvshow.replace(' ','+') + '&sort=4&userID=0'

        #must return an iterable
        #can be a list (like here) or a generator (use yield in that case)
        return [scrapy.Request(url=search, callback=self.parse)]

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
            )
