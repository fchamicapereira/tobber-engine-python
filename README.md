# tobber - a torrent grabber engine

Very basic project written in python 2.7 for searching torrents and grabbing the torrent file using my own personal tastes.

It's now torified with tor and polipo.

<b>Compatible torrent sites</b>
- https://zooqle.com (work in progress)
- https://nyaa.patsu.cat

<b>Tools:</b>
- [Scrapy](https://scrapy.org/)
- [Tor](https://www.torproject.org/)
- [Polipo](https://wiki.archlinux.org/index.php/Polipo)

## Requirements
- Python 2.6
- Pip for easy installation of the other requirements
- Tor
- Pilopo

## Installation

`$pip install -r requirements.txt`

## Starting

Run this command, substituting the `${flags}` for the actual flags you want to use.

`$python ignition.py ${flags}`


To get information about all the program flags:

`$python ignition.py -h`
