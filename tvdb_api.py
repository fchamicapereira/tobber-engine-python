# season.py

import requests
import json
import datetime

class Tvdb_api:
    def __init__(self):
        with open('tvdb_api.config') as api_file:
            self.api = json.load(api_file)
            self.headers = {
                "Content-Type":     "application/json",
                "Accept":           "application/json",
                "Authorization":    "Bearer " + self.api['token']
            }
            self.apiMsg = "ERROR: Not a valid request.\n"
            self.updateToken = "Error in the request. Requesting new token\n"

    def make_req(self, query):

        # make request
        res = requests.get(query, headers=self.headers)

        if res.status_code not in [200, 401]:
            print self.apiMsg
            raise ValueError

        if res.status_code != 401:
            return res

        if self.req_new_token() != 401:
            res = requests.get(query, headers=self.headers)

            if res.status_code not in [200, 401]:
                print self.apiMsg
                raise ValueError

            return res

        print 'Couldn\'t refresh the token. Making request to the /login page for a new token'


    def authenticate(self):

        # {api}/login
        query = self.api['site'] + '/login'

        info = {
            "apikey":   self.api['apikey'],
            "username": self.api['username'],
            "userkey":  self.api['userkey']
        }

        header = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        # make request
        res = requests.post(query, data=info, headers=header)


        print 'New token:'
        print res.json()


        if res.status_code == 401:
            print 'ERROR: Couldn\'t ask for a new token in the /login route'
            exit()

        self.api['token'] = res.json()['token']

        # store the new token in the tvdb_api.config
        with open('tbdv_api.config') as api_file:
            json.dump(self.api, api_file)

        print '\nMust update tvdb user page to accept this token'
        exit()


    def req_new_token(self):

        # {api}/refresh_token
        query = self.api['site'] + '/refresh_token'

        # make request
        res = requests.get(query, headers=self.headers)

        if res.status_code == 401:
            return res.status_code

        self.api['token'] = res.json()['token']
        self.headers['Authorization'] = 'Bearer ' + res.json()['token']

        # store the new token in the tvdb_api.config
        with open('tbdv_api.config') as api_file:
            json.dump(self.api, api_file)

        return res.status_code

    def getSeriesID(self,name):

        # {api}/search/series?name={show_name}
        query = self.api['site'] + '/search/series?name=' + name.replace(' ','%20')

        # make request
        res = self.make_req(query)

        # take the id of the first one (dirty, I know)
        return res.json()['data'][0]['id']

    def getSeriesInfo(self,name):

        # get ID
        seriesID = str(self.getSeriesID(name))

        # {api}/search/series?name={show_name}
        query = self.api['site'] + '/series/' + seriesID + '/episodes'

        # make request
        res = self.make_req(query)

        if res.status_code not in [200, 401]:
            print "[getSeriesID] " + self.apiMsg
            raise ValueError

        return res.json()

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

        for item in data:

            # there's not a release date for this episode yet
            if len(item['firstAired']) == 0:
                continue

            # verify if this episode has already been released or not
            ep_release_date = datetime.datetime.strptime(item['firstAired'],'%Y-%m-%d')
            today = datetime.datetime.today()

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
