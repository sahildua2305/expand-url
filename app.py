#!/usr/bin/env python
# -*- coding: utf-8 -*-

import bottle
from bottle import route, run, request, default_app
import httplib
import urlparse
import json
import urllib
from sys import argv

def expandURL(url):
    urls = [url]
    return unshorten_me(url, urls)

def unshorten_me(url, url_list):
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

@route('/')
def index():
    return "Hello from Sahil!"

@route('/encode/<url>', method='GET')
def encode(url=""):
    return urllib.quote_plus(url)

@route('/expand')
def expand(url = ""):
    url = request.query.get('url', '')
    if url == "":
        return {"success" : False,
            "start_url" : url,
            "final_url" : "",
            "url_list" : []
            }
    url_list = expandURL(url)
    return {"success" : True,
            "start_url" : url,
            "final_url" : url_list[-1],
            "url_list" : url_list
            }

bottle.run(host='0.0.0.0', port=argv[1])

# application = default_app()

# if __name__ == "__main__":
#     run(host='0.0.0.0', port=80)