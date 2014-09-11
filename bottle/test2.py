from bottle import route, run

@route('/expand-url/<url>', method='GET')
def expand(url = "http://example.com"):
    return {"success" : False,
            "start_url" : url,
            "final_url" : "",
            "url_list" : []
            }

run(host='localhost', port=8080, debug=True)
