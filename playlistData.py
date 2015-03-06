"""
Script to extract data from studio d'essai playlists.
At the moment, I have 'print' commands as feedback. These will eventually be converted so that they output to a file.
"""

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
                re_artist = re.compile('1.\s\[?([\w\s\d]+)[\]\w]')
                artist = re_artist.search(track).group(1)
                print(artist)
#               brainz link finder
                re_brainz = re.compile(r'(\]\((\S+musicbrainz.org/\S+)\))')
                brainz = re_brainz.search(track).group(2)
                print(brainz)
#               featured artist
                re_featArtist = re.compile('feat\.\s\[?([\w\s\d]+)\](\((\S+musicbrainz.org\S+)\))?')
                if re_featArtist.search(track) is None: pass
                else:
                    featArtist = re_featArtist.search(track).group(1)
                    featArtistBrainz = re_featArtist.search(track).group(3)
                    print(featArtist)
                    print(featArtistBrainz)
#               track title
                re_title = re.compile('\s[-]\s([\w\s]+)\s\(')
                title = re_title.search(track).group(1)
#               the remainder (best to do with one regex, as it's super regular)
                re_otherInf = re.compile('\(_(.+)_,\s+(.+),\s+(.+),\s+(.+)\)')
                album = re_otherInf.search(track).group(1)
                label = re_otherInf.search(track).group(2)
                year = re_otherInf.search(track).group(3)
                country = re_otherInf.search(track).group(4)
                print(album, label, year, country)
