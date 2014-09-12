import requests

r = requests.get('http://localhost:8080/expand-url', params={'url':'http://tuq.in/myspeed'})
print r.content
