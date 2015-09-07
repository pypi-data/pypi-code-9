
import httplib2
import json

def sentences():
    h = httplib2.Http()
    (resp_headers, content) = h.request('http://more.handlino.com/sentences.json', 'GET')
    return json.loads(content.decode('utf-8'))
