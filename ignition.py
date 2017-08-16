import subprocess
import json

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

def sort_and_store():
    top = 5

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
    subprocess.check_output(['scrapy','crawl','nyaa'])
    if not sort_and_store():
        print '\nERROR --- Couldn\'t scrap the site'
