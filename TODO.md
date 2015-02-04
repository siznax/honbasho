TODO
====

Automerge Japanese and English comments
---------------------------------------

In the past, Sumo Kyokai has provided English commentary on the
highlights, but they have not for the last couple of basho. So I've
been crawling both the English and Japanese highlights pages, and then
merging the comments by hand. See, for example: 

* [201411/en/data.json](https://github.com/siznax/honbasho/blob/master/201411/en/data.json)
* [201411/jp/data.json](https://github.com/siznax/honbasho/blob/master/201411/jp/data.json)

Automate this...

1. crawl the [English](http://www.sumo.or.jp/en/honbasho/topics/ko_torikumi15/list) highlights
2. download the mp4s
3. generate "highlights.html"
4. create "en/" and move *.[html,json,txt] into it,
5. repeat (1-4) for the [Japanese](http://www.sumo.or.jp/honbasho/topics/ko_torikumi15/list) highlights
6. merge <tt>en/highlights.html</tt> and <tt>jp/highlights.html</tt>


@siznax

