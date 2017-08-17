#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# author: Blue Cuenca <blue.cuenca@gmail.com>

import requests
import html2text
from bs4 import BeautifulSoup
from slugify import slugify


def get_metrolyrics_url(title, artist):
    url_pattern = u"http://www.metrolyrics.com/{}-lyrics-{}.html"
    return url_pattern.format(slugify(title), slugify(artist))


def fetch_soup(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    return soup


def get_lyrics(title, artist):
    url = get_metrolyrics_url(title, artist)
    soup = fetch_soup(url)

    lyrics_p = soup.find_all('p', attrs={'class': 'verse'})

    # join P's
    lyrics = unicode.join(u'', map(unicode, lyrics_p))
    return html2text.html2text(lyrics)


def test():
    pass


def main():
    print(get_lyrics("Truly Madly Deeply", "Savage Garden"))

if __name__ == "__main__":
    import sys
    sys.exit(main())
