import scrapy
from tobber.items import Torrent
from tobber.spiders.indexer import Indexer

class Zooqle(Indexer):
    name = "zooqle"

    def start_requests(self):
        print 'Zooqle is scrapying...'

        self.site = "https://zooqle.com"
        urls = []
        sortBySize = "&s=sz&v=t&sd=d"
        search = self.site + "/search?q="

        for title in self.title:
            urls.append(search + title)

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        #xPath rules
        table   = response.xpath('//table//tr')
        title   = table.xpath('./td[contains(@class,"text-trunc text-nowrap")]//a[contains(@class," small")]')
        href    = table.xpath('./td//a[@class=" small"]/@href')
        peers   = table.xpath('./td//div[contains(@class,"progress prog")]/@title')
        magnet  = table.xpath('./td//a[@title="Magnet link"]/@href')
        torrent = table.xpath('./td//a[@title="Generate .torrent"]/@href')
        size    = table.xpath('./td//div[@class="progress prog prog-narrow trans90"]//div[@class="progress-bar prog-blue prog-l"]/text()')

        for i in range(len(table)):

            # this is a hack
            # the title's text comes with <hl> tags that are
            # troublessome, so this will remove all the
            # garbage
            prettyTitle = title[i].extract().split('>',1)[1][:-4]
            prettyTitle = prettyTitle.replace('<hl>','').replace('</hl>','')

            # Seeders : X | Leechers: Y
            peersTuple = peers[i].re(r'(\d+).* (\d+)')

            yield Torrent(
                title       = prettyTitle,
                magnet      = magnet[i].extract().encode('ascii','ignore'),
                torrent     = self.site + torrent[i].extract().encode('ascii','ignore'),
                size        = size[i].extract().replace('\n','').encode('ascii','ignore'),
                seeders     = peersTuple[0].encode('ascii','ignore'),
                leechers    = peersTuple[1].encode('ascii','ignore'),
                href        = self.site + href[i].extract().encode('ascii','ignore'),
                site        = self.name
            )
