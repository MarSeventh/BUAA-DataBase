import pprint, requests, json

URL_ROOT = 'http://127.0.0.1:8000/'

data = {'username' : '泽连斯基', 'Pid' : '8', 'checkName' : '肝功能检查'}

d = {'room' : '201'}

r = requests.post(URL_ROOT+'api/getPatient', json=d)
pprint.pprint(r.json())


