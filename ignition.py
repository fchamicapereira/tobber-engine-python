# -*- coding: utf-8 -*-

import scrapy
import json
import argparse
import pymongo
from pprint import pprint

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from tobber.spiders.indexer import Indexer

from tobber.spiders.anime.nyaa import Nyaa
from tobber.spiders.tv_movies.zooqle import Zooqle

class Ignition:

    def __init__(self):
        args = self.process_args()
        self.run_crawler(args)
        self.open_mongo()
        self.sort(args.n)
        self.dump_collection()
        self.close_mongo()

    def sort_file(self, n):

        with open('torrents.jl') as data_file:
            torrents = json.load(data_file)['torrents']

        if len(torrents) == 0:
            return False

        ordered = sorted(torrents, key=lambda torrents: torrents['score'], reverse=True)

        for i in range(n - 1,-1,-1):
            print 'Place: ', i + 1
            print json.dumps(ordered[i], indent=4, sort_keys=True)

        return True

    def open_mongo(self):
        self.settings    = get_project_settings()
        self.client      = pymongo.MongoClient(self.settings['MONGODB_SERVER'], self.settings['MONGODB_PORT'])
        self.db          = self.client[self.settings['MONGODB_DB']]
        self.collection  = self.db[self.settings['MONGODB_COLLECTION']]

    def close_mongo(self):
        self.client.close()

    def sort(self, n):
        result = self.collection.find().sort("score", pymongo.DESCENDING)

        counter = 1
        for doc in result:
            if counter > n:
                break
            print '\n\nPlace: ', counter
            pprint(doc, width=-1)
            counter += 1

    def dump_collection(self):
        self.collection.drop()

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
        parser.add_argument('-l', '--log', action='store_true', help="show log in stdout")

        # parse args and return
        return parser.parse_args()

    def run_crawler(self, args):

        #join all the search words
        search = ' '.join(args.search)

        settings = get_project_settings()
        process = CrawlerProcess(settings)

        custom_settings = {}

        if args.torify:

            #torify tobber
            custom_settings["DOWNLOADER_MIDDLEWARES"] =  {
                    'tobber.middlewares.UserAgentMiddleware': 400,
                    'tobber.middlewares.ProxyMiddleware': 410,
                    'tobber.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None
            }

        if args.log == False:
            custom_settings["LOG_FILE"] = 'tobber.log'

        Indexer.custom_settings = custom_settings

        if args.anime:
            process.crawl(Nyaa, title=search, season=args.season)

        else:
            process.crawl(Zooqle, title=search, season=args.season)

        process.start()


def main():
    Ignition()

if __name__ == "__main__":
    main()
