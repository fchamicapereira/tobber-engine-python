# tobber - a torrent grabber engine

Very basic project written in python 2.7 for searching torrents and grabbing the torrent file using my own personal tastes.

It's now torified with tor and polipo.

## Compatible torrent sites
- https://zooqle.com
- https://nyaa.patsu.cat

## Requirements
- Python 2.7
- Pip for easy installation of the other requirements
- Tor (only if you want to torify tobber)
- Pilopo (only if you want to torify tobber)
- MongoDB

## Installation

Using pip:

`$pip install -r requirements.txt`

## Starting

Run `$python ignition.py ${flags}`, substituting the `${flags}` for the actual flags you want to use.

To get information about all the program flags:

`$python ignition.py -h`
