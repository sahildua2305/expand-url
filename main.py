import httplib
import urlparse

def unshorten_me(url):
    parsed = urlparse.urlparse(url)
    h = httplib.HTTPConnection(parsed.netloc)
    h.request('HEAD', parsed.path)
    response = h.getresponse()
    if response.status/100==3 and response.getheader('location'):
        return unshorten_me(response.getheader('location'))
    else:
        return url

#print unshorten_me('http://bit.ly/1whCayD')
print unshorten_me('http://tuq.in/KxEp')
