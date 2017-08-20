#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# author: Blue Cuenca <blue.cuenca@gmail.com>

import requests
import html2text
import eyed3
from glob import glob
from time import sleep
from bs4 import BeautifulSoup
import slugify


def myslugify(source):
    chars_to_remove = [",", "'", ".", "(", ")"]
    s = ''.join([c for c in source if c not in chars_to_remove])
    return slugify.slugify(s)


def get_metrolyrics_url(title, artist):
    url_pattern = u"http://www.metrolyrics.com/{}-lyrics-{}.html"
    return url_pattern.format(myslugify(title), myslugify(artist))


def fetch_soup(url):
    tries = 4
    soup = None
    while True:
        try:
            success = True
            r = requests.get(url)
        except requests.exceptions.ConnectionError:
            tries = tries - 1
            success = False
        if not success:
            print("sleeping for 500us")
            sleep(0.5)
        if success or (tries == 0):
            break

    soup = BeautifulSoup(r.text, "html.parser")

    return soup


def _get_lyrics(soup):
    h1 = soup.find('h1')
    if h1 and (h1.text == u'404 - Page Not Found'):
        return None
    else:
        lyrics_p = soup.find_all('p', attrs={'class': 'verse'})

        # join P's
        lyrics = unicode.join(u'', map(unicode, lyrics_p))
        return html2text.html2text(lyrics)


def get_lyrics_from(title, artist):
    url = get_metrolyrics_url(title, artist)
    soup = fetch_soup(url)
    return _get_lyrics(soup)


def get_lyrics(url):
    return _get_lyrics(fetch_soup(url))


def get_mp3(filename):
    return eyed3.load(filename)


def set_lyrics(filename):
    mp3 = get_mp3(filename)
    c = mp3.tag.comments.get(u'')
    lyrics = None
    if c:
        url = c.text
        lyrics = get_lyrics(url)
    if lyrics is None:
        lyrics = get_lyrics_from(mp3.tag.title, mp3.tag.artist)

    # if lyrics and not mp3.tag.lyrics:
    #    mp3.tag.lyrics.set(lyrics)
    #    mp3.tag.save()
    # else:
    #    print("has lyrics already, not setting")
    if lyrics and isinstance(lyrics, unicode):
        mp3.tag.lyrics.set(lyrics)
        mp3.tag.save()
        return True
    else:
        return False


def test():
    pass


def main():
    eyed3.log.setLevel("ERROR")
    # print(get_lyrics("Truly Madly Deeply", "Savage Garden"))
    # set_lyrics("Alone.mp3")
    for fname in glob("*.mp3"):
        # print "processing ", fname
        if not set_lyrics(fname):
            mp3 = get_mp3(fname)
            print "%s %s" % (fname, get_metrolyrics_url(mp3.tag.title,
                                                        mp3.tag.artist))

if __name__ == "__main__":
    import sys
    sys.exit(main())
