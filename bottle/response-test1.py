import requests

r = requests.get('http://localhost:8080/expand-url/http')
print r.content
