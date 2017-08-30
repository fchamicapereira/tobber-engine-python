import scrapy
from tobber.items import Torrent
from tobber.spiders.indexer import Indexer

class _1337x(Indexer):
    name = "1337x"

    def start_requests(self):
        print '1337x is scrapying...'

        self.site = "https://1337x.to"
        urls = []
        search = self.site + "/search/"
        page = '/1/'

        for title in self.title:
            urls.append(search + title.replace('%20','+') + page)

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_table)


    # in this spider I need 2 parsers, one for the table information
    # and other for the magnet and torrent links, since they're not
    # provided in the table
    # because of that, tobber needs to visit the torrent site
    # to extract the missing information

    def parse_table(self, response):

        #xPath rules
        table    = response.xpath('//table[@class="table-list table table-responsive table-striped"]//tbody//tr')
        title    = table.xpath('//td[@class="coll-1 name"]//a[not (@class="icon")]/text()')
        href     = table.xpath('//td[@class="coll-1 name"]//a[not (@class="icon")]/@href')
        seeders  = table.xpath('//td[contains(@class,"coll-2 seeds")]/text()')
        leechers = table.xpath('//td[contains(@class,"coll-3 leeches"]/text()')
        size     = table.xpath('//td[contains(@class,"coll-4 size")]/text()')

        for i in range(len(table)):

            torrent_site = self.site + href[i].extract().encode('ascii','ignore')

            data = {
                "title":    title[i].extract().encode('ascii', 'ignore'),
                "href":     torrent_site,
                "seeders":  seeders[i].extract().encode('ascii','ignore'),
                "leechers": leechers[i].extract().encode('ascii','ignore'),
                "size":     size[i].extract().encode('ascii','ignore')
            }

            # decided to not use this method (commented below), it increased the crawling time by A LOT
            # so now i dont get the magnet and torrent for this indexer
            # yield scrapy.Request(url=torrent_site, callback=self.parse_torrent_page,meta={'data': data})

            yield Torrent(
                title       = data['title'],
                size        = data['size'],
                seeders     = data['seeders'],
                leechers    = data['leechers'],
                href        = data['href'],
                site        = self.name
            )

    def parse_torrent_page(self, response):

        data = response.meta.get('data')

        response = response.xpath('//div[@class="col-9 page-content"]//div//div//div//ul//li//a/@href').extract()

        yield Torrent(
            title       = data['title'],
            magnet      = response[0],
            torrent     = response[2],
            size        = data['size'],
            seeders     = data['seeders'],
            leechers    = data['leechers'],
            href        = data['href'],
            site        = self.name
        )
