import pprint, requests, json

data = {'username': 'admin', 'password': 'buaadb'}

response = requests.post('http://127.0.0.1:8000/test/login', json=data)

pprint.pprint(response.json())
