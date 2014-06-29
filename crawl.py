#!/usr/bin/env python2.7

__author__ = "siznax"
__version__ = "Jun 2014"

import argparse
import json
import lxml.html
import requests
import urlparse


class CrawlBasho:

  def __init__(self, url):
    self.url = urlparse.urlparse(url)
    self.base = "%s://%s" % (self.url.scheme, self.url.netloc)
    self.list = self.base + self.url.path
    self.basho = self.base + self.url.path.replace('/list', '')
    self.data = []

  def crawl(self):
    """
    get URLs and details for each highlight
    """
    self.get_hrefs()
    for item in self.data:
      self.get_details(item)

  def get_hrefs(self):
    """
    get detail URLs for all highlights listed
    """
    page = requests.get(self.list).text
    doc = lxml.html.fromstring(page)
    for elm in doc.cssselect("a.arr"):
      href = "%s/%s" % (self.basho, elm.attrib['href'])
      self.data.append({"href": href})

  def get_details(self, data):
    """
    get description and movie URL for this highlight
    """
    page = requests.get(data['href']).text
    doc = lxml.html.fromstring(page)

    txt = doc.cssselect("p.txt")[0].text
    data['txt'] = txt

    onclick = doc.cssselect("p.movie a")[0].attrib['onclick']
    movie = str(onclick.split("'")[1])
    data['movie'] = "%s/%s" % (self.base, movie)


def print_json(data):
    print json.dumps(data,
                     sort_keys=True,
                     indent=4,
                     separators=(',', ': '))


def main(args):
  """
  crawl grand sumo hightlights and output metadata as JSON
  [
    {
      "href":  <details_url>
      "movie": <mp4_url>
      "txt":   <description>
    },
    ...
  ]
  """
  basho = CrawlBasho(args.url)
  # print vars(basho)
  basho.crawl()
  print_json(basho.data)


if __name__ == "__main__":
    argp = argparse.ArgumentParser()
    argp.add_argument('url', help='honbasho highlights URL')
    main(argp.parse_args())
