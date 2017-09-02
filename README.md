# tobber - a torrent grabber engine

Very basic project written in python 2.7.12 for searching torrents and grabbing the torrent file using my own personal tastes.

## Compatible torrent sites
- https://zooqle.com
- https://nyaa.patsu.cat
- https://eztv.ag
- https://1337x.to

## Dependencies

### Required

- Python 2.7

### Not required

- Pip for easy installation of the other requirements
- Tor (only if you want to torify tobber)
- Polipo (only if you want to torify tobber)
- MongoDB (only if you want to use mongo database instead of outputing to a file)

## Installation

Using pip:

`$pip install -r requirements.txt`

## Starting

Run `$python ignition.py ${flags}`, substituting the `${flags}` for the actual flags you want to use.

To get information about all the program flags:

`$python ignition.py -h`

## Arguments

All the arguments are optional, except for the "search" argument.

- `-h` / `--help`

  Output all the possible arguments and how to use them

- search

  No tag must be written. It's the only mandatory argument. It'll be all the text that is not followed by a flag.

  `python ignition Game of Thrones` - search = Game of Thrones

- `-n` / `-N`

  Number of torrents you want to see in the end. It requires a number. The default value is 5.

  `python ignition Game of Thrones -n 2`

- `-s` / `--season`

  Number of the season you want to search. It requires a number, and has no default value.

  `python ignition.py Game of Thrones -s 3`

- `-f` / `--file`

  File that will receive all the torrent's information. Must be a path, and end with the extension '.json'. If used, tobber will not use mongodb for storing the information, but instead the file you provided. If just the tag is used but followed by no path, tobber will use the default file (torrents.json in the project path).

  `python ignition.py Game of Thrones -f /home/user/documents/something.json`

- `-t` / `--torify`

  Make tobber use tor and polipo. You must have tor and polipo running in the background.

  `python ignition.py Game of thrones -n 3 -s 1 -t`

- `-a` / `--anime`

  Make tobber search in the anime spiders.

  `python ignition.py One Piece -a`

- `-l` / `--log`

  Output to the console all the information tobber can display, for example connections, requests and debugging information.

  `python ignition.py -l Game of Thrones`

- `-le` / `--last-episode`

    Getting the latest aired episode of the content inserted in the search field.

    `python ignition.py -le Game of Thrones`

- `--server`

    Run tobber in server mode.

    `python ignition.py -le Game of Thrones --server`

- `-r` / `--rules`

    Give the path of a score_rules.json file containing rules for scoring the torrents.

    `python ignition.py -le Game of Thrones -r /home/somebody/documents/my_rules.json`


## Tweaking

To make your own rules for torrent choosing, edit the 'score_rules.json' file.

Each torrent is given a certain number of points that will give them advantadge against the others. The formula starts by taking the log of the size and add the sum of the properties of the torrent multiplied by the value corresponding to that property. These values are discriminated in the 'score_rules.json' file. By raising the values in some properties, you'll make that group of properties more important than the others.
