## HOW-TO archive grand sumo highlights

update config file:

    {
        "201411": {
    	"source": "http://www.sumo.or.jp/en/honbasho/topics/ko_torikumi15/list",
    	"date": "4 December 2014",
    	"title": "Kyūshū 2014 (November) Grand Sumo Highlights",
    	"archive": "honbasho-2014-kyushu"
        },
    ...

crawl and download:

    # get highlights metadata
    $ crawl.py {selector} > data.json

    # download movies and text
    $ download.py {dest} data.json

    # make HTML index
    $ mkindex.py data.json {selector} > index.html

upload to Internet Archive:

    * S3 upload *.mp4, *.txt to archive.org
    * mediatype: movies
    * collection: opensource_media
    * DERIVE all after last upload
    * S3 upload index.html

### Archived highlights

<table>
<tr>
 <th>Highlights
 <th>Archive
<tr>
 <td><a href="https://archive.org/download/honbasho-2014-kyushu/index.html">Kyūshū 2014</a> (November)
 <td><a href="https://archive.org/details/honbasho-2014-kyushu">honbasho-2014-kyushu</a>
<tr>
 <td><a href="https://archive.org/download/honbasho-2014-aki/index.html">Aki 2014</a> (September)
 <td><a href="https://archive.org/details/honbasho-2014-aki">honbasho-2014-aki</a>
<tr>
 <td><a href="https://archive.org/download/honbasho-2014-nagoya/index.html">Nagoya 2014</a> (July)
 <td><a href="https://archive.org/details/honbasho-2014-nagoya">honbasho-2014-nagoya</a>
<tr>
 <td><a href="https://archive.org/download/honbasho-2014-natsu/index.html">Natsu 2014</a> (May)
 <td><a href="https://archive.org/details/honbasho-2014-natsu">honbasho-2014-natsu</a>
</table>


@siznax
