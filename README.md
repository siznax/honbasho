honbasho
========

Archive [Grand Sumo](http://www.sumo.or.jp/en/) tournament
hightlights, as they are removed by Nihon Sumo Kyokai before each
tournament.

Usage
-----

Update config file, e.g.:

    "201501": {
	"source": "http://www.sumo.or.jp/en/honbasho/topics/ko_torikumi15/list",
	"date": "3 Feb 2015",
	"title": "Hatsu 2015 (January) Grand Sumo Highlights",
	"archive": "honbasho-2015-hatsu"

Crawl and Download:

```shell
# get highlights metadata
$ crawl.py {selector} > data.json

# download movies and text
$ download.py {dest} data.json

# make HTML index
$ mkindex.py data.json {selector} > index.html
```

Upload to Internet Archive, e.g.:

 * Upload with [siznax/iatools](https://github.com/siznax/iatools)
 * DERIVE all after last upload
 * S3 upload index.html

```shell
$ workon honbasho
(honbasho)$ iatools/s3upload.py honbasho-2015-hatsu index.html\
 -m "mediatype:movies" "collection:opensource_media"
(honbasho)$ iatools/s3upload.py honbasho-2015-hatsu *.txt
(honbasho)$ iatools/s3upload.py honbasho-2015-hatsu *.mp4
```

See archived highlights at <https://siznax.github.io/honbasho >

@siznax
