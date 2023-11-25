import pprint, requests, json

URL_ROOT = 'http://127.0.0.1:8000/'

data = {'Pid' : '6', 'Did' : '5'}

r = requests.post(URL_ROOT+'test/Registration', json=data)

pprint.pprint(r.json())


