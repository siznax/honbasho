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
      print "  " + href
      self.data.append({"href": href})


  def get_details(self, data):
    """
    get description and movie URL for this highlight
    """
    fname = self.dest + "-{0:02d}".format(self.index) + ".html"
    page = self.get_html(fname, data['href'])
    doc = lxml.html.fromstring(page)

    txt = doc.cssselect("p.txt")[0].text
    print "  txt: " + txt
    data['txt'] = txt

    onclick = doc.cssselect("p.movie a")[0].attrib['onclick']
    movie = str(onclick.split("'")[1])
    href = "%s/%s" % (self.base, movie)
    print "  movie: " + href
    data['movie'] = href


def print_json(data):
    print json.dumps(data,
                     sort_keys=True,
                     indent=4,
                     separators=(',', ': '))


def main(args):
  """
  crawl grand sumo hightlights and output metadata as JSON
      href:  <details_url>
      movie: <mp4_url>
      txt:   <description>
  """
  with open("config.json") as fp:
    config = json.loads(fp.read())
    basho = CrawlBasho(config[args.selector]["source"])
    basho.dest = args.selector
    # print vars(basho)
    basho.crawl()
    # print_json(basho.data)

if __name__ == "__main__":
    argp = argparse.ArgumentParser()
    argp.add_argument('selector', help='config.json selector')
    main(argp.parse_args())
