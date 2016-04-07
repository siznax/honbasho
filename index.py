#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

__author__ = "siznax"
__version__ = "Jun 2014"

import argparse
import json
import os
import sys

from string import Template

CSS = """
body {
    background:whitesmoke;
    margin:auto;
    width:500px;
    padding:64px;
    padding-top:0;
    font-family:meiryo, verdana, Osaka;
}
.movie {
    background:white;
    padding:8px;
    padding-bottom:32px;
}
.movie p:first-of-type {
    margin-top:0;
}
.movie video {
    width:480px;
    height:270px;
    background:#000;
}
"""
DETAILS = 'https://archive.org/details'
DOWNLOAD = 'https://archive.org/download'
HTML_TEMPLATE = Template("""<!doctype html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=500">
<title>${title}</title>
<style>${css}</style>
</head>
<h1>${title}</h1>
""")
MOVIE_DIV = Template("""<div class=movie>
${text}
${video}
</div>
""")
TAIL = Template("""<p>
Source: <a href="${source}">${source}</a><br>
Archive: <a href="${details}/${archive}">${details}/${archive}</a><br>
Code: <a href="${code}">${code}</a><br>
Date: ${date}<br>
</p>""")
TEXT_TEMPLATE = Template("""<p>
<b>Highlight ${hnum}</b>
<p id="jp">${jp}</p>
<p id="en">${en}</p>
</p>""")
VIDEO_TEMPLATE = Template("""<video controls preload="none"
 poster="${poster}">
 <source src="${mp4}" type="video/mp4">
 <source src="${ogg}" type="video/ogg">
Your browser does not support the video tag.
</video>""")


def print_divs(item, archive):
  mp4 = item['movie'].split('/')[-1]
  ogg = mp4.replace('.mp4', '.ogg')
  poster = mp4.replace('.mp4', '.gif')
  mp4_url = "%s/%s/%s" % (DOWNLOAD, archive, mp4)
  ogg_url = "%s/%s/%s" % (DOWNLOAD, archive, ogg)
  poster_url = "%s/%s/%s" % (DOWNLOAD, archive, poster)
  video = VIDEO_TEMPLATE.substitute(
    poster=poster_url,
    mp4=mp4_url, ogg=ogg_url)
  text = TEXT_TEMPLATE.substitute(
    hnum=os.path.splitext(mp4)[0].split('_')[-1],
    jp=item['txt']['jp'],
    en=item['txt']['en'])
  print MOVIE_DIV.substitute(video=video, text=text).encode('utf-8')


def main(config):

  if not os.path.exists(config["data_file"]):
    print "ERROR data_file not found: " + config["data_file"]
    sys.exit(os.EX_NOINPUT)
  title = config["title"].encode("utf-8").replace("Grand", "<br>Grand")
  print HTML_TEMPLATE.substitute(title=title, css=CSS)

  with open(config["data_file"]) as fp:
    data = json.loads(fp.read())
    for item in data:
      print_divs(item, config["archive"])

  print TAIL.substitute(source=config["source"],
                        date=config["date"],
                        details=DETAILS,
                        archive=config["archive"],
                        code=config["code"])
  sys.exit(os.EX_OK)

if __name__ == "__main__":
  argp = argparse.ArgumentParser()
  argp.add_argument('data_file', help='JSON output from crawl.py (CrawlBasho)')
  argp.add_argument('selector', help='config.json selector')
  args = argp.parse_args()

  config_file = "config.json"

  if os.path.exists(config_file):
    with open(config_file) as fp:
      cfg_json = json.loads(fp.read())
      config = cfg_json[args.selector]
      config["data_file"] = args.data_file
      config["code"] = cfg_json["code"]
      main(config)

  print "ERROR config file not found: " + config_file
  sys.exit(os.EX_NOINPUT)
