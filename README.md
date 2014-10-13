honbasho - archive grand sumo highlights

update config file:

    {
        "201409": {
        "source": "http://www.sumo.or.jp/en/honbasho/topics/ko_torikumi15/list",
        "date": "11 October 2014",
        "title": "Aki 2014 (September) sumo highlights",
        "archive": "honbasho-2014-aki"
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

    * S3 upload to archive.org
    * mediatype: movies
    * collection: opensource_media
    * DERIVE all after last upload
    * S3 upload index.html

Archived highlights

 * [Aki 2014 (September)](https://archive.org/download/honbasho-2014-aki) [[archive](https://archive.org/details/honbasho-2014-aki)]
 * [Nagoya 2014 (July)](https://archive.org/download/honbasho-2014-nagoya) [[archive](https://archive.org/details/honbasho-2014-nagoya)]
 * [Natsu 2014 (May)](https://archive.org/download/honbasho-2014-natsu) [[archive](https://archive.org/details/honbasho-2014-natsu)]


@siznax
