import pprint, requests, json

URL_ROOT = 'http://127.0.0.1:8000/'

data = {'Pid' : '6', 'Did' : '5'}

r = requests.get(URL_ROOT+'api/showAllDrug/')

pprint.pprint(r.json())


