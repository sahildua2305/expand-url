from bottle import route, run
import httplib
import urlparse
import json
import urllib

def expandURL(url):
    urls = [url]
    return unshorten_me(url, urls)

def unshorten_me(url, url_list):
    parsed = urlparse.urlparse(url)
    h = httplib.HTTPConnection(parsed.netloc)
    h.request('HEAD', parsed.path)
    response = h.getresponse()
    if response.status/100==3 and response.getheader('location'):
        url_list.append(response.getheader('location'))
        return unshorten_me(response.getheader('location'), url_list)
    else:
        if url not in url_list:
            url_list.append(url)
        return url_list

@route('/encode/<url>', method='GET')
def encode(url=""):
    return urllib.quote_plus(url)

@route('/expand-url/<url>', method='GET')
def expand(url = "http://example.com"):
    url_list = expandURL('http://tuq.in/KxEp')
    return {"success" : False,
            "start_url" : url,
            "final_url" : "",
            "url_list" : url_list
            }

run(host='localhost', port=8080, debug=True)
