#!/usr/bin/env python2.7

import argparse
import json
import os
import sys

from string import Template

CSS = """
body {
    margin:auto;
    width:720px;
    padding:32px;
    padding-top:0;
    font-family:meiryo, verdana, Osaka;
}
.movie {
    padding:8px;
    padding-bottom:32px;
}
.movie p:first-of-type {
    margin-top:0;
}
.movie video {
    width:640px;
    height:360px;
    background:#000;
}
"""
DETAILS = 'https://archive.org/details'
DOWNLOAD = 'https://archive.org/download'

HTML_TEMPLATE = Template("""<!doctype html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=720">
<title>${title}</title>
<style>${css}</style>
</head>
<h1>${title}</h1>
""")

MOVIE_DIV = Template("""<div id="${num}" class="movie">
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

TEXT_TEMPLATE = Template("""<p><b>Highlight ${num}</b></p>
<p class="jp">${jp}</p>
<p class="en">${en}</p>""")

VIDEO_TEMPLATE = Template("""<video
 controls preload="none" poster="${poster}">
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
    num = int(os.path.splitext(mp4)[0].split('_')[-1])
    video = VIDEO_TEMPLATE.substitute(poster=poster_url,
                                      mp4=mp4_url, ogg=ogg_url)
    text = TEXT_TEMPLATE.substitute(num=num,
                                    jp=item['txt']['jp'],
                                    en=item['txt']['en'])
    print MOVIE_DIV.substitute(num=num, video=video, text=text).encode('utf-8')


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
    argp.add_argument('data_file',
                      help='JSON crawl data')
    argp.add_argument('selector',
                      help='basho.json selector')
    args = argp.parse_args()

    basho_file = "basho.json"
    if os.path.exists(basho_file):
        with open(basho_file) as fp:
            bjson = json.loads(fp.read())
            basho = bjson[args.selector]
            basho["data_file"] = args.data_file
            basho["code"] = bjson["code"]
            main(basho)

    print "ERROR: file not found: " + basho_file
    sys.exit(os.EX_NOINPUT)
