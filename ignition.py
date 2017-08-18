# -*- coding: utf-8 -*-

import scrapy
import json
import argparse

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from tobber.spiders.indexer import Indexer

from tobber.spiders.anime.nyaa import Nyaa
from tobber.spiders.tv_movies.zooqle import Zooqle

class Ignition:

    def __init__(self):
        args = self.process_args()
        self.run_crawler(args)
        self.sort_and_store(args.n)

    def sort_and_store(self, n):

        with open('torrents.jl') as data_file:
            torrents = json.load(data_file)['torrents']

        if len(torrents) == 0:
            return False

        ordered = sorted(torrents, key=lambda torrents: torrents['score'], reverse=True)

        for i in range(n - 1,-1,-1):
            print 'Place: ', i + 1
            print json.dumps(ordered[i], indent=4, sort_keys=True)

        return True

    def process_args(self):

        # create args logic
        parser = argparse.ArgumentParser(description='tobber - a torrent grabber engine')

        # need input
        parser.add_argument('search', nargs='+', type=str, help="title of the content you want to search")
        parser.add_argument('-n', type=int, default=5, help="amount of torrents I will display")
        parser.add_argument('-s', '--season', type=int, default=-1, help="search for entire season")

        # don't need input
        parser.add_argument('-t', '--torify', action='store_true', help="torify the tobber")
        parser.add_argument('-a', '--anime', action='store_true', help="use this if searching for anime")

        # parse args and return
        return parser.parse_args()

    def run_crawler(self, args):

        #join all the search words
        search = ' '.join(args.search)

        settings = get_project_settings()
        process = CrawlerProcess(settings)

        if args.torify:

            #torify tobber
            Indexer.custom_settings = {
                "DOWNLOADER_MIDDLEWARES": {
                    'tobber.middlewares.UserAgentMiddleware': 400,
                    'tobber.middlewares.ProxyMiddleware': 410,
                    'tobber.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None
                }
            }

        if args.anime:
            process.crawl(Nyaa, title=search, season=args.season)

        else:
            process.crawl(Zooqle, title=search, season=args.season)

        process.start()


def main():
    Ignition()

if __name__ == "__main__":
    main()
