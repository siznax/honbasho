honbasho
========

Archive [Grand Sumo](http://www.sumo.or.jp/) tournament highlights,
as they are _removed_ :sob: before each new tournament. 


Update the config
-----------------

Update ``basho.json`` with latest source and metadata, e.g.

```
"201607": {
    "source": "http://www.sumo.or.jp/EnHonbashoTopicsKoTorikumi15/wrap",
    "date": "12 Aug 2016",
    "title": "Nagoya 2016 (July) Grand Sumo Highlights",
    "archive": "honbasho-201607-nagoya",
    "description": "<b>Nagoya 2016</b>\n\nNagoya, Aichi Prefectural Gymnasium\n\nJuly 10, 2016 - July 24, 2016\n\n"
```


Crawl and download
------------------

Get highlights metadata:

```shell
$ mkdir {dest}
$ crawl.py {selector} > {dest}/data.json
```

Download movies and text:

```shell
$ download.py {dest} {dest}/data.json
```

Make highlights HTML index:

```shell
$ index.py {dest}/data.json {selector} > {dest}/highlights.html
```


Upload to the Internet Archive
------------------------------

* Add a description for the archive page in ``basho.json``
* Move crawl HTML out of {dest}/
* Make sure {selector} and {dest} have same name (e.g. 201607)

Review metadata changes to be made:

```shell
$ upload.py {selector}
```

Upload files and modify metadata:

```shell
$ upload.py {selector} -u  # upload files
$ upload.py {selector} -m  # modify metadata
```


Update project pages
--------------------

* Checkout `gh-pages` branch and update ``index.html``
* See https://siznax.github.io/honbasho


Thanks to the [Internet Archive](https://archive.org/) for hosting,
and @jjjake for the excellent
[internetarchive](https://github.com/jjjake/internetarchive)
python library.


@siznax
