#!/usr/bin/env python

from __future__ import print_function

import argparse
import json
import lxml.html
import os
import requests
import urlparse
import sys

from settings import Default


class Honbasho:
    """Crawl Grand Sumo hightlights"""

    def __init__(self, dest, basho, user_agent):
        url = urlparse.urlparse(basho["source"])
        self.base = "%s://%s" % (url.scheme, url.netloc)
        self.data = []
        self.dest = dest
        self.source = basho["source"]
        self.user_agent = user_agent

    def crawl(self):
        """get URLs and details for each highlight"""
        self.get_hrefs()
        for index, item in enumerate(self.data):
            self.index = index
            self.get_details(item, "en")
            self.get_details(item, "jp")

    def get_html(self, fname, url):
        """GET HTML or read from file"""
        fname = os.path.join(self.dest, fname)
        if os.path.exists(fname):
            with open(fname, "r") as fp:
                html = fp.read()
                print("+ read %d bytes from %s" % (fp.tell(),
                                                   fname),
                      file=sys.stderr)
                return html

        print("GET " + url, file=sys.stderr)
        headers = {'User-Agent': self.user_agent}
        html = requests.get(url, headers=headers).text.encode('utf-8')
        if not os.path.exists(self.dest):
            os.mkdir(self.dest)
        with open(fname, "w") as fp:
            fp.write(html)
            print("+ wrote %d bytes to %s" % (fp.tell(), fname),
                  file=sys.stderr)
            return html

    def get_hrefs(self):
        """get detail URLs for all highlights listed"""
        html = self.get_html("list.html", self.source)
        doc = lxml.html.fromstring(html)
        for elm in doc.cssselect("a.arr"):
            en = urlparse.urljoin(self.base, elm.attrib['href'])
            jp = en.replace('/EnHonbashoTopicsKoTorikumi15/',
                            '/ResultDataKoTorikumi15/')
            hrefs = {"href": {"en": en, "jp": jp}}
            print("  en: " + en, file=sys.stderr)
            print("  jp: " + jp, file=sys.stderr)
            self.data.append(hrefs)

    def get_description(self, doc, lang):
        day = doc.cssselect("td.day")[0].text
        win = doc.cssselect("td.win a")[0].text
        east = doc.cssselect("td.brLb a")[0].text
        west = doc.cssselect("td.brRb a")[0].text
        if east == win:
            east += "*"
        if west == win:
            west += "*"
        tech = doc.cssselect("td.decide")[0].text
        text = doc.cssselect("p.txt")[0].text
        fmt = "%s %s %s (%s) %s"
        if lang == "en":
            fmt = "%s day %s %s (%s) %s"
        desc = fmt % (day, east, west, tech, text)
        desc = desc.strip()
        print("  desc: " + desc, file=sys.stderr)
        return desc

    def get_movie_href(self, doc):
        onclick = doc.cssselect("p.movie a")[0].attrib['onclick']
        movie = str(onclick.split("'")[1])
        href = urlparse.urljoin(self.base, movie)
        print("  movie: " + href, file=sys.stderr)
        return href

    def get_details(self, data, lang):
        """get description and movie URL for one highlight"""
        fname = "%s-%s-%s.html" % (self.dest, lang,
                                   "{0:02d}".format(self.index))
        page = self.get_html(fname, data['href'][lang])
        doc = lxml.html.fromstring(page)
        if 'txt' not in data:
            data['txt'] = {}
        data['txt'][lang] = self.get_description(doc, lang)
        data['movie'] = self.get_movie_href(doc)


def main(args):
    with open("basho.json") as fp:
        basho = json.loads(fp.read())
    hb = Honbasho(args.selector,
                  basho[args.selector],
                  Default.USER_AGENT)
    hb.crawl()
    print(json.dumps(hb.data,
                     ensure_ascii=False,
                     encoding='utf-8',
                     sort_keys=True,
                     indent=4,
                     separators=(',', ': ')).encode('utf8'))


if __name__ == "__main__":
    argp = argparse.ArgumentParser()
    argp.add_argument('selector', help='basho.json selector')
    main(argp.parse_args())
