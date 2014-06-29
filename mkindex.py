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
  margin:32px;
  margin-bottom:64px;
  height:240px;
  font-size:x-large;
}
.movie video {
  float:left;
  margin-right:32px;
  width:427px;
  height:240px;
  background:#ccc;
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
TAIL = Template("""<p>${date} <a href="${url}">${url}</a></p>""")
TEXT_TEMPLATE = Template("""
<b>${bold}</b>: ${text}
""")
VIDEO_TEMPLATE = Template("""<video controls preload="none">
  <source src="${mp4}" type="video/mp4">
  <source src="${ogg}" type="video/ogg">
Your browser does not support the video tag.
</video>""")


def print_divs(item, archive):
  mp4 = item['movie'].split('/')[-1]
  ogg = mp4.replace('.mp4', '.ogg')
  mp4_url = "%s/%s/%s" % (DOWNLOAD, archive, mp4)
  ogg_url = "%s/%s/%s" % (DOWNLOAD, archive, ogg)
  bold = os.path.splitext(mp4)[0].title().replace('_', ' ')
  video = VIDEO_TEMPLATE.substitute(mp4=mp4_url, ogg=ogg_url)
  text = TEXT_TEMPLATE.substitute(bold=bold, text=item['txt'])
  print MOVIE_DIV.substitute(video=video, text=text)


def main(args):
  if not os.path.exists(args.data_file):
    print "data_file not found: " + args.data_file
    sys.exit(os.EX_USAGE)

  print HTML_TEMPLATE.substitute(title=args.title, css=CSS)

  data = json.load(open(args.data_file))
  for item in data:
    print_divs(item, args.archive)

  print TAIL.substitute(date=datetime.datetime.now().strftime("%c"),
                        url=args.source)


if __name__ == "__main__":
  argp = argparse.ArgumentParser()
  argp.add_argument('data_file', help='JSON output from crawl.py (CrawlBasho)')
  argp.add_argument('title', help='html title')
  argp.add_argument('archive', help='Internet Archive identifier')
  argp.add_argument('source', help='source URL')

  main(argp.parse_args())
