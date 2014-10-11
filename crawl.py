#!/usr/bin/env python2.7

__author__ = "siznax"
__version__ = "Oct 2014"

import argparse
import json
import lxml.html
import os
import requests
import urlparse


class CrawlBasho:

  def __init__(self, dest, config):
    self.dest = dest
    self.url = urlparse.urlparse(config["source"])
    self.base = "%s://%s" % (self.url.scheme, self.url.netloc)
    self.list = self.base + self.url.path
    self.basho = self.base + self.url.path.replace('/list', '')
    self.data = []

  def crawl(self):
    """
    get URLs and details for each highlight
    """
    self.get_hrefs()
    for index, item in enumerate(self.data):
      self.index = index
      self.get_details(item)


  def get_html(self, fname, url):
    """
    read HTML from disk or send GET request
    """
    fname = os.path.join(self.dest, fname)
    if os.path.exists(fname):
      with open(fname, "r") as fp:
        html = fp.read()
        print "+ read %d bytes from %s" % (fp.tell(), fname)
        return html

    print "GET " + url
    html = requests.get(url).text.encode('utf-8')
    if not os.path.exists(self.dest):
      os.mkdir(self.dest)
    with open(fname, "w") as fp:
      fp.write(html)
      print "+ wrote %d bytes to %s" % (fp.tell(), fname)
      return html


  def get_hrefs(self):
    """
    get detail URLs for all highlights listed
    """
    html = self.get_html("list.html", self.list)
    doc = lxml.html.fromstring(html)
    for elm in doc.cssselect("a.arr"):
      href = "%s/%s" % (self.basho, elm.attrib['href'])
      print "  detail: " + href
      self.data.append({"href": href})


  def get_description(self, doc):
    day = doc.cssselect("td.day")[0].text
    text = doc.cssselect("p.txt")[0].text
    east = doc.cssselect("td.brLb a")[0].text
    west = doc.cssselect("td.brRb a")[0].text
    tech = doc.cssselect("td.decide")[0].text
    desc = (text + " %s day %s %s (%s)" % (day, east, west, tech)).strip()
    print "  desc: " + desc
    return desc


  def get_movie_href(self, doc):
    onclick = doc.cssselect("p.movie a")[0].attrib['onclick']
    movie = str(onclick.split("'")[1])
    href = "%s/%s" % (self.base, movie)
    print "  movie: " + href
    return href


  def get_details(self, data):
    """
    get description and movie URL for this highlight
    """
    fname = self.dest + "-{0:02d}".format(self.index) + ".html"
    page = self.get_html(fname, data['href'])
    doc = lxml.html.fromstring(page)
    data['txt'] = self.get_description(doc)
    data['movie'] = self.get_movie_href(doc)


def print_json(data):
    print json.dumps(data,
                     sort_keys=True,
                     indent=4,
                     separators=(',', ': '))


def main(args):
  """
  crawl grand sumo hightlights and output metadata as JSON
      href:  <details_url>
      txt:   <description>
      movie: <mp4_url>
  """
  with open("config.json") as fp:
    config = json.loads(fp.read())
    basho = CrawlBasho(args.selector, config[args.selector])
    # print vars(basho)
    basho.crawl()
    print_json(basho.data)

if __name__ == "__main__":
    argp = argparse.ArgumentParser()
    argp.add_argument('selector', help='config.json selector')
    main(argp.parse_args())
