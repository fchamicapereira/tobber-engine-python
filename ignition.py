import subprocess
import json

def print_compact_torrent(torrent):
    print 'title:      ', torrent['title']
    print 'size:       ', torrent['size']
    print 'properties:'

    if 'resolution' in torrent['properties']:
        print '\tresolution:  ', torrent['properties']['resolution']

    if 'source' in torrent['properties']:
        print '\tsource:      ', torrent['properties']['source']

    if 'audio' in torrent['properties']:
        print '\taudio:       ', torrent['properties']['audio']

    if 'encoding' in torrent['properties']:
        print '\tencoding:    ', torrent['properties']['encoding']

    if 'format' in torrent['properties']:
        print '\tformat:       ', torrent['properties']['format']

def sort_and_store():
    top = 5

    with open('torrents.jl') as data_file:
        torrents = json.load(data_file)['torrents']

    ordered = sorted(torrents, key=lambda torrents: torrents['score'], reverse=True)

    for i in range(top - 1,-1,-1):
        print '\n--------------------------------------------------------\n'
        print 'Place: ', i + 1, '\n'
        print_compact_torrent(ordered[i])
        #print json.dumps(ordered[i], indent=4, sort_keys=True)


subprocess.check_output(['scrapy','crawl','nyaa'])
sort_and_store()
