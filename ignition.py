import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from tobber.spiders.spider_init import Spider_init
import json

from tobber.spiders.anime.nyaa import Nyaa
from tobber.spiders.tv_movies.zooqle import Zooqle

def print_if_exists(torrent,key, level):
    string = ''

    for _ in range(level):
        string = string + '\t'

    string = string + key + ':'

    while len(string) < 15:
        string = string + ' '

    if key in torrent:
        print string + torrent[key]

def print_compact_torrent(torrent):
    print 'title:      ', torrent['title']
    print 'size:       ', torrent['size']
    print 'score:      ', torrent['score']
    print 'properties:'

    for key in torrent['properties']:
        print_if_exists(torrent['properties'],key, 1)

def sort_and_store(top):
    with open('torrents.jl') as data_file:
        torrents = json.load(data_file)['torrents']

    if len(torrents) == 0:
        return False

    ordered = sorted(torrents, key=lambda torrents: torrents['score'], reverse=True)

    for i in range(top - 1,-1,-1):
        print '\n------------------------------ PLACE',i + 1,'------------------------------\n'
        print_compact_torrent(ordered[i])
        #print json.dumps(ordered[i], indent=4, sort_keys=True)

    return True


if __name__ == "__main__":

    settings = get_project_settings()
    process = CrawlerProcess(settings)
    
    if False:
        Spider_init.custom_settings = {
            "HTTP_PROXY": 'http://127.0.0.1:8123',
            "DOWNLOADER_MIDDLEWARES": {
                'tobber.middlewares.UserAgentMiddleware': 400,
                'tobber.middlewares.ProxyMiddleware': 410,
                'tobber.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None
            }
        }

    process.crawl(Zooqle)
    process.start()

    if not sort_and_store(10):
        print '\nERROR --- Couldn\'t scrap the site'
