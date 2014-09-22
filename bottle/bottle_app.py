from bottle import route, run, request, default_app
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

@route('/hello/')
def hello():
    return "Hello from Sahil!"

@route('/encode/<url>', method='GET')
def encode(url=""):
    return urllib.quote_plus(url)

@route('/expand-url', method='GET')
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

application = default_app()

if __name__ == "__main__":
    run(host='0.0.0.0', port=80)
