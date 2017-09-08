import scrapy
import re
from tobber.items import Torrent
from tobber.spiders.indexer import Indexer

class Shanaproject(Indexer):
    name = "shanaproject"

    def start_requests(self):
        print 'Shanaproject is scrapying...'

        self.site = "https://www.shanaproject.com"
        urls = []

        for title in self.title:
            urls.append(self.site + "/search/?title=" + title.replace('%20','+') + '&subber=')

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        #xPath rules
        row = response.xpath('//div[@class="release_block"]')

        for i in range(1,len(row)):

            title       = row.xpath('./div[@class="rel_x"]//div[@class="release_text_contents"]/text()')
            category    = row.xpath('./div[@class="release_row_first"]//div[@class="release_subber"]//div//a/text()')
            torrent     = row.xpath('./div[@class="release_row_first"]//a[@type="application/x-bittorrent"]/@href')
            size        = row.xpath('./div[@class="release_row_first"]//div[contains(@class,"release_size")]/text()')

            yield Torrent(
                title       = self.extract_data(title),
                torrent     = self.extract_data(torrent),

                # size came with numbers and letters all together, this just adds a space between
                #size        = " ".join(re.split('(\d+\.*\d+)',self.extract_data(size)))[1:],
                size = size.extract()[0],

                category    = self.extract_data(category),

                # shanaproject doesnt have a torrent directory, so just give the searched page
                href        = str(response).split('<200 ')[1].split('>')[0],

                site        = self.name,
                counter     = i
            )
