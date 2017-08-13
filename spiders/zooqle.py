import scrapy
from tobber.items import Torrent

class Zooqle(scrapy.Spider):
    name = "zooqle"

    def start_requests(self):
        self.site = "https://zooqle.com"

        tvshow = "game of thrones"
        sortBySize = "&s=sz&v=t&sd=d"

        search = self.site + "/search?q=" + tvshow.replace(' ','%20') + sortBySize

        #must return an iterable
        #can be a list (like here) or a generator (use yield in that case)
        return [scrapy.Request(url=search, callback=self.parse)]

    # pretty printing
    def printTorrent(self,torrent):
        print '\n{'
        print '\t Title: ' + torrent['title']
        print '\t href: ' + torrent['href']
        print '\t Torrent: ' + torrent['torrent']
        print '\t Magnet: ' + torrent['magnet']
        print '\t Size: ' + torrent['size']
        print '\t Seeders: ' + str(torrent['seeders'])
        print '\t Leechers: ' + str(torrent['leechers'])
        print '}\n'

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
                magnet      = magnet[i].extract(),
                torrent     = self.site + torrent[i].extract(),
                size        = size[i].extract().replace('\n',''),
                seeders     = peersTuple[0],
                leechers    = peersTuple[1],
                href        = self.site + href[i].extract()
            )
