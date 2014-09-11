import httplib
import urlparse

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

#print unshorten_me('http://bit.ly/1whCayD')
#print unshorten_me('http://tuq.in/KxEp')
print expandURL('http://tuq.in/KxEp')
