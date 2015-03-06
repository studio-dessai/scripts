""" Script to extract data from studio d'essai playlists. """

import re # for regex
import os # for filesystem
import csv

for i in os.listdir():
    if i[-4].isnumeric(): #  tests for if i is a playlist file by checking date in filename
        f = open(i)
        fi = f.read()

        tracks = fi.splitlines()
        for i in tracks:
            if str(i).__contains__('Playlist for'): tracks.remove(i)

        # defines date variable; allowable because only one date per file
        re_date = re.compile('\d{4}\.\d{2}\.\d{2}')
        date = re_date.search(fi).group()

        for track in tracks:
            if len(track) < 1:
                continue
            else:
#               artist finder
                re_artist = re.compile('(1.\s\[?([\w\s\d]+)[\]\w])')
                artist = re_artist.search(track).group(2)
                print(artist)
#               brainz link finder
                re_brainz = re.compile('(\([\w\s\d]+musicbraiz\.org[\w\s\d]+)\)')
                brainz = re_brainz.search(track).group(1)
                print(brainz)

#         print(re_artist.search(track).group())
