import pprint, requests

response = requests.get('http://127.0.0.1:8000/api/showAllDrug/')

pprint.pprint(response.json())

response = requests.get('http://127.0.0.1:8000/api/departmentList/')

pprint.pprint(response.json())