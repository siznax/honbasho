#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

__author__ = "siznax"
__version__ = "Jun 2014"

import argparse
import json
import os
import sys
import datetime

from string import Template

CSS = """
.movie {
  clear:both;
}
.movie p {
  font-size:x-large;
}
.movie video {
  float:left;
  height:240px;
  width:427px;
  background:#000;
  margin-right:1em;
  margin-bottom:2em;
}
"""
DOWNLOAD = 'https://archive.org/download'
HTML_TEMPLATE = Template("""<!doctype html>
<head>
<meta charset=utf-8>
<title>${title}</title>
<style>${css}</style>
</head>
<h1>${title}</h1>
""")
MOVIE_DIV = Template("""<div class=movie>
${video}
${text}
</div>
""")
TAIL = Template("""<br clear="both">
<p>
Source: <a href="${source}">${source}</a><br>
Code: <a href="${code}">${code}</a><br>
Archive: <a href="https://archive.org/details/${archive}">${archive}</a><br>
Date: ${date}<br>
</p>""")

TEXT_TEMPLATE = Template("""
<p><b>${bold}</b>: ${text}</p>
""")
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
  bold = os.path.splitext(mp4)[0].split('_')[-1]
  video = VIDEO_TEMPLATE.substitute(
    poster=poster_url, mp4=mp4_url, ogg=ogg_url)
  text = TEXT_TEMPLATE.substitute(bold=bold, text=item['txt'])
  print MOVIE_DIV.substitute(video=video, text=text)


def main(args):

  if not os.path.exists(args["data_file"]):
    print "data_file not found: " + args["data_file"]
    sys.exit(os.EX_USAGE)

  print HTML_TEMPLATE.substitute(title=args["title"], css=CSS)

  data = json.load(open(args["data_file"]))
  for item in data:
    print_divs(item, args["archive"])

  print TAIL.substitute(source=args["source"], 
                        date=args["date"],
                        archive=args["archive"],
                        code=args["code"])

if __name__ == "__main__":
  argp = argparse.ArgumentParser()
  argp.add_argument('data_file', help='JSON output from crawl.py (CrawlBasho)')
  argp.add_argument('selector', help='config.json selector')
  args = argp.parse_args()

  with open("config.json") as fp:
    config = json.loads(fp.read())
    _input = config[args.selector]
    _input["data_file"] = args.data_file
    _input["code"] = config["code"]
    main(_input)

