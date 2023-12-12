import pprint, requests, json

URL_ROOT = 'http://127.0.0.1:8000/'

data = {'username' : '泽连斯基', 'Pid' : '17', 'Statement' : '新冠肺炎阳性，伴随肺部轻微感染，建议转院治疗'}

dataforMed = {'MedcineList' : ['风油精 (瓶)', '云南白药气雾剂 (瓶)', '布洛芬 (盒)'], 'AmountList' : [1, 2, 3], 'Pid' : '17', 'username' : '张三'}

d = {'room' : '201'}

d1 = {'Medicine' : '冰糖', 'Amount' : 100, 'Price' : 1, 'Description' : '用于治疗感冒'}

r = requests.post(URL_ROOT+'api/addMedicine/', json=d1)
pprint.pprint(r.json())


