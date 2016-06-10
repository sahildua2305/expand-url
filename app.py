#!/usr/bin/env python
# -*- coding: utf-8 -*-

import bottle, requests
from bottle import route, run, request, default_app
import httplib
import urlparse
import json
import urllib
from sys import argv

@route('/')
def index():
    return "To expand a link, send a GET request to <a href='/expand?url=http://goo.gl/i4NyPz'>/expand?url=&lt;your_short_url&gt;</a>!"

@route('/encode', method='GET')
def encode(url=""):
    url = request.query.get('url', '')
    return urllib.quote_plus(url)

@route('/expand')
def expand(url = ""):
    url = request.query.get('url', '')

    if url == "":
        return {
            "success": False,
            "start_url": url,
            "final_url": "",
            "url_list": []
        }

    url_list = expandURL(url)

    if len(url_list) == 0:
        success = False
        final_url = ""
    else:
        success = True
        final_url = url_list[-1]

    return {
        "success": success,
        "start_url": url,
        "final_url": final_url,
        "url_list": url_list
    }

def expandURL(url):
    urls = [url]
    return unshorten_me(url, urls)

def unshorten_me(url, url_list):
    try:
        requests.head(url, allow_redirects=True).url
    except:
        return list()
    else:
        parsed = urlparse.urlparse(url)
        h = httplib.HTTPConnection(parsed.netloc)
        h.request('HEAD', parsed.path)
        response = h.getresponse()
        if response.status/100==3 and response.getheader('location'):
            new_url = response.getheader('location')
            if new_url not in url_list:
                url_list.append(new_url)
            return unshorten_me(response.getheader('location'), url_list)
        else:
            if url not in url_list:
                url_list.append(url)
            return url_list

bottle.run(host='0.0.0.0', port=argv[1])
