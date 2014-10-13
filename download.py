#!/usr/bin/env python2.7

__author__ = "siznax"
__version__ = "Jun 2014"

import argparse
import json
import os
import pycurl
import sys


def write_text_file(fname, data):
  if not os.path.exists(fname):
    with open(fname, 'w') as fp:
      fp.write(data['txt'] + "\n")
      fp.write(data['href'] + "\n")
      print "  wrote %d byes to %s" % (fp.tell(), fname)
  else:
    print "  " + fname
  sys.stdout.flush()


def write_movie_file(fname, data):
  if not os.path.exists(fname):
    with open(fname, 'wb') as fp:
      print "CURL " + data['movie']
      curl = pycurl.Curl()
      curl.setopt(pycurl.URL, data['movie'])
      curl.setopt(pycurl.WRITEDATA, fp)
      curl.perform()
      curl.close()
      print "  wrote %d byes to %s" % (fp.tell(), fname)
  else:
    print "  " + fname
  sys.stdout.flush()


def download(item, dest):
  url = item['movie']
  movie_file = url.split('/')[-1]
  text_file = movie_file.replace(os.path.splitext(movie_file)[-1], '.txt')

  write_text_file(os.path.join(dest, text_file), item)
  write_movie_file(os.path.join(dest, movie_file), item)


def main(args):
  if not os.path.exists(args.data_file):
    print "data_file not found: " + args.data_file
    sys.exit(os.EX_USAGE)

  data = json.load(open(args.data_file))
  for item in data:
    download(item, args.dest)


if __name__ == "__main__":
  argp = argparse.ArgumentParser()
  argp.add_argument('dest', help='destination path')
  argp.add_argument('data_file', help='JSON output from crawl.py (CrawlBasho)')
  main(argp.parse_args())
