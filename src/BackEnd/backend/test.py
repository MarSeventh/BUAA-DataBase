import pprint, requests, json

URL_ROOT = 'http://127.0.0.1:8000/'

data = {'content' : "我的症状是脚踝扭伤"}

r = requests.post(URL_ROOT+'', json=data)


pprint.pprint(r.json())


