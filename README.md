honbasho - crawl grand sumo highlights


    # get highlights metadata
    $ BASHO=http://www.sumo.or.jp/en/honbasho/topics/ko_torikumi15/list
    $ crawl.py $BASHO > data.json

    # download movies and text
    $ download.py data.json

    # make HTML index
    $ mkindex.py data.json "Natsu 2014" honbasho-2014-natsu $BASHO > index.html

    # upload to Internet Archive


Archived highlights

 * [Nagoya 2014 (July)](https://archive.org/download/honbasho-2014-nagoya) [[archive](https://archive.org/details/honbasho-2014-nagoya)]
 * [Natsu 2014 (May)](https://archive.org/download/honbasho-2014-natsu) [[archive](https://archive.org/details/honbasho-2014-natsu)]


@siznax
