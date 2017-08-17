import scrapy
from tobber.items import Torrent
from tobber.spiders.spider_init import Spider_init

class Zooqle(Spider_init):
    name = "zooqle"

    def start_requests(self):
        self.site = "https://zooqle.com"

        tvshow = "game of thrones s01"
        sortBySize = "&s=sz&v=t&sd=d"

        search = self.site + "/search?q=" + tvshow.replace(' ','%20') + sortBySize

        #must return an iterable
        #can be a list (like here) or a generator (use yield in that case)
        return [scrapy.Request(url=search, callback=self.parse)]

    def parse(self, response):
        #xPath rules
        table   = response.xpath('//table//tr')
        title   = table.xpath('//td[contains(@class,"text-trunc text-nowrap")]//a[contains(@class," small")]')
        href    = title.xpath('//td//@href')
        peers   = table.xpath('//td//div[contains(@class,"progress prog")]/@title')
        magnet  = table.xpath('//td//a[@title="Magnet link"]/@href')
        torrent = table.xpath('//td//a[@title="Generate .torrent"]/@href')
        size    = table.xpath('//td//div[@class="progress prog prog-narrow trans90"]//div[@class="progress-bar prog-blue prog-l"]/text()')

        for i in range(len(table)):

            # this is a hack
            # the title's text comes with <hl> tags that are
            # troublessome, so this will remove all the
            # garbage
            prettyTitle = title[i].extract().split('>',1)[1][:-4]
            prettyTitle = prettyTitle.replace('<hl>','').replace('</hl>','')

            # Seeders : X | Leechers: Y
            peersTuple = peers[i].re(r'.*(\d+).*(\d+)')

            yield Torrent(
                title       = prettyTitle,
                magnet      = magnet[i].extract().encode('ascii','ignore'),
                torrent     = self.site + torrent[i].extract().encode('ascii','ignore'),
                size        = size[i].extract().replace('\n','').encode('ascii','ignore'),
                seeders     = peersTuple[0].encode('ascii','ignore'),
                leechers    = peersTuple[1].encode('ascii','ignore'),
                href        = self.site + href[i].extract().encode('ascii','ignore')
            )
