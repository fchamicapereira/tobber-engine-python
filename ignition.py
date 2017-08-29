# -*- coding: utf-8 -*-

import scrapy
import json
import argparse
import pymongo
import os

from pprint import pprint

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from tobber.spiders.indexer import Indexer

from tobber.spiders.tv_movies import *
from tobber.spiders.anime import *

from tvdb_api import Tvdb_api

class Ignition:

    def __init__(self):

        # getting the settings of the project (settings.py)
        self.settings = get_project_settings()

        # getting the tvdb instance
        self.tvdb = Tvdb_api(self.settings['TVDB_API_CONFIG'])

        # processing input arguments
        self.process_args()

        # meeting the arguments with the settings
        self.change_settings()

        # open mongo here just to check if mongod service is running
        # if it isn't, might as well not start crawling
        if self.args.file == None:
            self.open_mongo()
            self.dump_collection()

        # running the spiders
        self.run_crawler()

        if self.args.file:
            self.sort_file()

        else:

            if self.args.server == False:

                # working with the mongo db
                self.sort()

            # close mongo
            self.close_mongo()


    def open_mongo(self):
        HOST = self.settings['MONGODB_SERVER']
        PORT = self.settings['MONGODB_PORT']

        #timeout to 2 seconds
        TIMEOUT = 2

        try:
            self.client      = pymongo.MongoClient(host=HOST, port=PORT,serverSelectionTimeoutMS=TIMEOUT)
            self.db          = self.client[self.settings['MONGODB_DB']]
            self.collection  = self.db[self.settings['MONGODB_COLLECTION']]
            self.client.server_info()

        except pymongo.errors.ServerSelectionTimeoutError:
            print 'Mongod service is not running.'
            print 'If you don\'t want to use the mongo database, use the -f tag.'
            print 'Closing tobber.'
            exit()


    def close_mongo(self):
        self.client.close()

    def dump_collection(self):
        self.collection.drop()

    def sort_file(self):

        with open(self.args.file) as data_file:
            torrents = json.load(data_file)['torrents']

        if len(torrents) == 0:
            print 'No torrents were grabbed :('
            return

        ordered = sorted(torrents, key=lambda torrents: torrents['score'], reverse=True)

        for i in range(self.args.n):
            print '\nPlace: ', i + 1
            print json.dumps(ordered[i], indent=4, sort_keys=True)

    def sort(self):
        result = self.collection.find().sort("score", pymongo.DESCENDING)

        counter = 1
        for doc in result:
            if counter > self.args.n:
                break
            print '\n\nPlace: ', counter
            pprint(doc, indent=2, width=-1)
            counter += 1

    def process_args(self):

        torrents_file = os.getcwd() + os.path.sep + 'torrents.json'

        # create args logic
        parser = argparse.ArgumentParser(description='tobber - a torrent grabber engine')

        # need input
        parser.add_argument('search', nargs='+', type=str, help="title of the content you want to search")
        parser.add_argument('-n', type=int, default=5, help="amount of torrents I will display")
        parser.add_argument('-s', '--season', type=int, default=-1, help="search for entire season")
        parser.add_argument('-f', '--file', nargs='?', type=str,
            default=None, const=torrents_file, help="export to file instead of mongo (if path is given, it will use that)")

        # don't need input
        parser.add_argument('-t', '--torify', action='store_true', help="torify the tobber")
        parser.add_argument('-a', '--anime', action='store_true', help="use this if searching for anime")
        parser.add_argument('-l', '--log', action='store_true', help="show log in stdout")
        parser.add_argument('-le', '--last-episode', action='store_true', help="get the latest episode aired")
        parser.add_argument('--server', action='store_true', help="run in server mode")

        # parse args and return
        self.args = parser.parse_args()

    def change_settings(self):

        # join all the search words
        self.search = ' '.join(self.args.search)

        # using anime tag
        if self.args.anime:
            self.settings['ITEM_PIPELINES']['tobber.pipelines.english_anime.English_anime'] = 200

        # using a file instead of mongodb
        if self.args.file:
            if self.args.file.split('.')[-1] != 'json':
                print '---Error in the torrent\'s file name given---'
                print 'Please give a file instead of a path and make sure it has de .json extension'
                exit()

            self.settings['ITEM_PIPELINES']['tobber.pipelines.save.Save'] = 950

        else:
            self.settings['ITEM_PIPELINES']['tobber.pipelines.mongo.Mongo'] = 950

        # torifying
        if self.args.torify:

            #torify tobber
            self.settings["DOWNLOADER_MIDDLEWARES"]['tobber.middlewares.ProxyMiddleware'] = 410
            self.settings["DOWNLOADER_MIDDLEWARES"]['tobber.contrib.downloadermiddleware.useragent.UserAgentMiddleware'] = None

        # show log in the stdout instead of log file
        if self.args.log == False:
            self.settings["LOG_FILE"] = 'tobber.log'

        if self.args.last_episode:
            episode = self.tvdb.getLastEpisode(self.search)
            self.search = self.search + ' ' + episode

            print 'Searching for ' + self.search


    def run_crawler(self):

        process = CrawlerProcess(self.settings)

        if self.args.anime:
            process.crawl(Nyaa,  title=self.search, season=self.args.season, file=self.args.file)

        else:
            process.crawl(Zooqle, title=self.search, season=self.args.season, file=self.args.file)
            process.crawl(Eztv,   title=self.search, season=self.args.season, file=self.args.file)
            #process.crawl(_1337x, title=self.search, season=self.args.season, file=self.args.file)

        process.start()


def main():
    Ignition()

if __name__ == "__main__":
    main()
