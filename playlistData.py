#!/usr/bin/env python
"""
Script to extract data from studio d'essai playlists.
"""

import re # for regex
import os # for filesystem
import csv
from sys import argv

for i in argv[1:]:
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
            try:
#               artist finder
                re_artist = re.compile('1.\s\[?([\w\s\d]+)[\]\w]')
                artist = re_artist.search(track).group(1)

#               brainz link finder
                re_brainz = re.compile(r'(\]\((\S+musicbrainz.org\/\S+)\))')
                if re_brainz.search(track) is None: brainz = ""
                else: brainz = re_brainz.search(track).group(2)

#               featured artist
                re_featArtist = re.compile('feat\.\s\[?([\w\s\d]+)\](\((\S+musicbrainz.org\S+)\))?')
                if re_featArtist.search(track) is None:
                    featArtist = ""
                    featArtistBrainz = ""
                else:
                    featArtist = re_featArtist.search(track).group(1)
                    featArtistBrainz = re_featArtist.search(track).group(3)

#               track title
                re_title = re.compile('\s[-]\s([\s\w\d]+)\s\(')
                title = re_title.search(track).group(1)

#               the remainder (best to do with one regex, as it's super regular)
                re_otherInf = re.compile('\(_(.+)_,\s+(.+),\s+(.+),\s+(.+)\)')
                if re_otherInf.search(track) is None:
                    continue
                album = re_otherInf.search(track).group(1)
                label = re_otherInf.search(track).group(2)
                year = re_otherInf.search(track).group(3)
                country = re_otherInf.search(track).group(4)

                with open('dat.csv', 'a', newline='\n') as output:
                    # note! opening dat.csv with 'a' allows amending lines instead of writing over them.
                    datwriter = csv.writer(output, delimiter=',', quoting=csv.QUOTE_MINIMAL)
                    datwriter.writerow([date, artist, brainz, title, album, label, year, country])

        except:
                with open('dat.csv', 'a', newline='\n') as output:
                    datwriter = csv.writer(output, delimiter=',', quoting=csv.QUOTE_MINIMAL)
                    datwriter.writerow(['irregular: needs manual input'])
                continue
    f.close()
