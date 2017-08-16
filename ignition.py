import subprocess
import json

subprocess.check_output(['scrapy','crawl','nyaa'])

def sort_and_store():
    with open('torrents.jl') as data_file:
        torrents = json.load(data_file)['torrents']

    ordered = sorted(torrents, key=lambda torrents: torrents['score'], reverse=True)

    for i in range(5,-1,-1):
        print '\n--------------------------------------------------------\n'
        print 'Place: ', i + 1
        print json.dumps(ordered[i], indent=4, sort_keys=True)

sort_and_store()
