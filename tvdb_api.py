# season.py

import requests
import json
import datetime

class Tvdb_api:
    def __init__(self, config):

        # path to config file
        self.config = config

        with open(self.config) as api_file:
            self.api = json.load(api_file)
            self.headers = {
                "Content-Type":     "application/json",
                "Accept":           "application/json",
                "Authorization":    "Bearer " + self.api['token']
            }

            self.apiMsg = "[TVDB] ERROR: Not a valid request.\n"
            self.updateTokenMsg = "[TVDB] Requesting new token\n"

    def make_req(self, query):

        # make request
        res = requests.get(query, headers=self.headers)

        if res.status_code not in [200, 401]:
            print self.apiMsg
            exit()

        if res.status_code != 401:
            return res.json()

        if self.req_new_token() != 401:
            print self.updateTokenMsg
            res = requests.get(query, headers=self.headers)

            if res.status_code not in [200, 401]:
                print self.apiMsg
                exit()

            return res.json()

        print '[TVDB] Couldn\'t refresh the token. Making request to the /login page for a new token'
        self.authenticate()

        return requests.get(query, headers=self.headers).json()


    def authenticate(self):

        # {api}/login
        query = self.api['site'] + '/login'

        data = json.dumps({
            "apikey": self.api['apikey'].encode('utf-8'),
            "userkey": self.api['userkey'].encode('utf-8'),
            "username": self.api['username'].encode('utf-8')
        })

        header = {
            "Content-Type": "application/json"
        }

        # make request
        res = requests.post(query, data=data, headers=header)

        if res.status_code == 401:
            print '[TVDB] ERROR: Couldn\'t ask for a new token in the /login route'
            exit()

        # updating token
        self.update_token(res.json()['token'])

    def req_new_token(self):

        # {api}/refresh_token
        query = self.api['site'] + '/refresh_token'

        # make request
        res = requests.get(query, headers=self.headers)

        if res.status_code != 401:
            self.update_token(res.json()['token'])

        return res.status_code

    def update_token(self, token):
        self.api['token'] = token
        self.headers['Authorization'] = 'Bearer ' + token

        # store the new token in the tvdb_api.config
        with open(self.config, 'w') as api_file:
            json.dump(self.api, api_file, indent=4)

    def getSeriesID(self,name):

        # {api}/search/series?name={show_name}
        query = self.api['site'] + '/search/series?name=' + name.replace(' ','%20')

        # make request
        data = self.make_req(query)['data']

        if len(data) == 0:
            print 'Show not found'
            exit()

        if len(data) == 1:
            return data[0]['id']

        # grab the one that is still going on
        for show in data:
            if show['status'] == 'Continuing':
                return show['id']

        return data[0]['id']

    def getSeriesInfo(self,name):

        # get ID
        seriesID = str(self.getSeriesID(name))

        # {api}/search/series?name={show_name}
        query = self.api['site'] + '/series/' + seriesID + '/episodes'

        # make request
        return self.make_req(query)

    def countEpisodesOfSeason(self,name,season):

        # get ID
        info = self.getSeriesInfo(name)

        data = info['data']
        counter = 0

        for item in data:

            # Episode X in the name means it isn't out yet
            if item['airedSeason'] == season and 'Episode' not in item['episodeName']:
                counter += 1

        return counter

    def getLastEpisode(self, name):

        # get ID
        info = self.getSeriesInfo(name)

        data = info['data']

        season = 0
        episode = 0

        today = datetime.datetime.today()

        for item in data:

            # there's not a release date for this episode yet
            if len(item['firstAired']) == 0:
                continue

            # verify if this episode has already been released or not
            ep_release_date = datetime.datetime.strptime(item['firstAired'],'%Y-%m-%d')

            if today < ep_release_date:
                continue

            # get the latest season
            if item['airedSeason'] > season:
                season = item['airedSeason']
                episode = item['airedEpisodeNumber']
                continue

            #get the latest episode
            if item['airedEpisodeNumber'] > episode and item['airedSeason'] == season:
                episode = item['airedEpisodeNumber']

        if season < 10:
            wanted = 's0'
        else:
            wanted = 's'

        wanted += str(season)

        if episode < 10:
            wanted += 'e0'
        else:
            wanted += 'e'

        wanted += str(episode)

        return wanted
