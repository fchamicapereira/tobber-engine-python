# tobber - a torrent grabber engine

Very basic project written in python 2.7 for searching torrents and grabbing the torrent file using my own personal tastes.

It's now torified with tor and polipo.

## Compatible torrent sites
- https://zooqle.com
- https://nyaa.patsu.cat

## Dependencies
### Required
- Python 2.7

### Not required
- Pip for easy installation of the other requirements
- Tor (only if you want to torify tobber)
- Pilopo (only if you want to torify tobber)
- MongoDB (only if you want to use mongo database instead of outputing to a file)

## Installation

Using pip:

`$pip install -r requirements.txt`

## Starting

Run `$python ignition.py ${flags}`, substituting the `${flags}` for the actual flags you want to use.

To get information about all the program flags:

`$python ignition.py -h`

## Tweaking

To make your own rules for torrent choosing, edit the 'score_rules.json' file.

Each torrent is given a certain number of points that will give them advantadge against the others. The formula starts by taking the log of the size and add the sum of the properties of the torrent multiplied by the value corresponding to that property. These values are discriminated in the 'score_rules.json' file. By raising the values in some properties, you'll make that group of properties more important than the others.
