import pprint, requests, json

URL_ROOT = 'http://127.0.0.1:8000/'

data = {'name' : "药"}

r = requests.post(URL_ROOT+'api/searchMedicineList/', json=data)


pprint.pprint(r.json())


