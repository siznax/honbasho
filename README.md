honbasho - crawl grand sumo highlights


    # get highlights metadata
    $ BASHO=http://www.sumo.or.jp/en/honbasho/topics/ko_torikumi15/list
    $ crawl.py $BASHO > data.json

    # download movies and text
    $ download.py data.json

    # make HTML index
    $ mkindex.py data.json "Natsu 2014" honbasho-2014-natsu $BASHO > index.html


see, for example:

> <https://archive.org/download/honbasho-2014-natsu/data.json>
> <https://archive.org/download/honbasho-2014-natsu>     
> <https://archive.org/details/honbasho-2014-natsu>


@siznax
