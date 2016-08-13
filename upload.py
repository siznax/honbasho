#!/usr/bin/env python
"""
Interactively upload basho files to Internet Archive

Expects:
    basho.json[dir] => {archive, description}
    dir/data.json => {movie, txt: {en}}
    dir/highlights.html
    dir/*.mp4
"""

import argparse
import glob
import json
import os
import sys

from internetarchive import upload, modify_metadata


def get_metadata(_id, _dir):
    """returns {target,title} metadata for each file in item"""
    meta = {}
    with open(_dir + "/data.json") as fp:
        data = json.loads(fp.read())
    for path in glob.glob(_dir + "*.mp4"):
        name = os.path.basename(path)
        meta[name] = {'target': "files/%s" % name}
        meta[name]['title'] = get_title(data, name)
        meta[name]["identifier"] = _id
    return meta


def get_title(data, name):
    """returns movie title metadata from crawl datafile given filename"""
    for i, item in enumerate(data):
        if name in data[i]["movie"]:
            return item["txt"]["en"]


def pretty(data):
    """pretty-print JSON data"""
    return json.dumps(data,
                      sort_keys=True,
                      separators=(',', ': '),
                      indent=2)


def update_metadata(_id, meta, for_real=False):
    print "modify_metadata(%s)" % _id
    for item in meta:
        _md = {'title': meta[item]["title"]}
        tgt = meta[item]["target"]
        if for_real:
            print ("modify_metadata(%s, metadata=%s, target='%s')"
                   % (_id, _md, tgt))
            modify_metadata(_id, metadata=_md, target=tgt)
        else:
            print "  target=%s metadata=%s" % (tgt, _md)


def main(args):
    with open("basho.json") as fp:
        basho = json.loads(fp.read())

    _id = basho[args.basho]["archive"]
    _dir = os.path.join(args.basho, '')  # ensure trailing slash
    desc = basho[args.basho]["description"] + basho["description"]
    item = {'collection': 'opensource_media',
            'mediatype': 'movies',
            'description': desc}

    print _id,
    print pretty(item)

    if args.upload:
        print "=" * 72
        print "upload(%s, %s, metadata=%s)" % (_id, _dir, item)
        if raw_input("Continue with upload? (y/N): ") == 'y':
            upload(_id, _dir, metadata=item, verbose=True)

    meta = get_metadata(_id, _dir)
    update_metadata(_id, meta)

    if args.metadata:
        print "=" * 72
        if raw_input("Update metadata? (y/N): ") == 'y':
            update_metadata(_id, meta, for_real=True)


if __name__ == "__main__":
    argp = argparse.ArgumentParser("Upload highlights")
    argp.add_argument('basho', help="basho.json selector")
    argp.add_argument('-m', '--metadata', action='store_true',
                      help="actually DO modify_metadata!")
    argp.add_argument('-u', '--upload', action='store_true',
                      help="actually DO upload!")
    args = argp.parse_args()
    main(args)
