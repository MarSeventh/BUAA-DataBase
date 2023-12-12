import pprint, requests, json

URL_ROOT = 'http://127.0.0.1:8000/'

data = {'username' : '泽连斯基'}

r = requests.post(URL_ROOT+'api/getDoctorSchedule/', json=data)
pprint.pprint(r.json())


