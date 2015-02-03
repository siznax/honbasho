honbasho
========

Archive [Grand Sumo](http://www.sumo.or.jp/en/) tournament
highlights, as they are removed by _Nihon Sumo Kyokai_ before each 
tournament.

Usage
-----

Update config file, e.g.:

```json
[
    "201501": {
	"source": "http://www.sumo.or.jp/en/honbasho/topics/ko_torikumi15/list",
	"date": "3 Feb 2015",
	"title": "Hatsu 2015 (January) Grand Sumo Highlights",
	"archive": "honbasho-2015-hatsu"
    }, ...
]
```

Crawl and Download:

```shell
# get highlights metadata
$ crawl.py {selector} > data.json

# download movies and text
$ download.py {dest} data.json

# make HTML index
$ mkindex.py data.json {selector} > index.html
```

Upload to Internet Archive:

 * Upload with [siznax/iatools](https://github.com/siznax/iatools) (below)
 * DERIVE all after last upload

```shell
(honbasho)$ iatools/s3upload.py {item} index.html\
 -m "mediatype:movies" "collection:opensource_media"
(honbasho)$ iatools/s3upload.py {item} *.txt
(honbasho)$ iatools/s3upload.py {item} *.mp4
```

See archived highlights => https://siznax.github.io/honbasho

@siznax
