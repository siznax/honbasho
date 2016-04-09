#!/usr/bin/env python2.7

from __future__ import print_function

import argparse
import json
import os
import pycurl
import sys

from settings import Default


def write_movie_file(fname, data):
    if not os.path.exists(fname):
        with open(fname, 'wb') as fp:
            print("GET " + data['movie'], file=sys.stderr)
            curl = pycurl.Curl()
            curl.setopt(pycurl.URL, str(data['movie']))
            curl.setopt(pycurl.WRITEDATA, fp)
            curl.setopt(pycurl.USERAGENT, Default.USER_AGENT)
            curl.perform()
            curl.close()
            print("+ wrote %d byes to %s" % (fp.tell(), fname),
                  file=sys.stderr)
    else:
        print("  " + fname, file=sys.stderr)
    sys.stdout.flush()


def download(item, dest):
    url = item['movie']
    movie_file = url.split('/')[-1]
    write_movie_file(os.path.join(dest, movie_file), item)


def main(args):
    if not os.path.exists(args.data_file):
        print("data_file not found: " + args.data_file, file=sys.stderr)
        sys.exit(os.EX_USAGE)

    data = json.load(open(args.data_file))
    for item in data:
        download(item, args.dest)


if __name__ == "__main__":
    """download movie files for upload to archive.org"""
    argp = argparse.ArgumentParser()
    argp.add_argument('dest',
                      help='destination path')
    argp.add_argument('data_file',
                      help='JSON output from crawl.py (CrawlBasho)')
    main(argp.parse_args())
