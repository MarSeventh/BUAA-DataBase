import json

import requests


class uploader:
    token = ''

    def __int__(self):
        email = '2601666034@qq.com'
        password = 'zjy815419zjy'
        base_url = 'https://imgbed.sanyue.site/api/v1'
        token_url = f'{base_url}/tokens'

        response = requests.post(token_url, json={'email': email, 'password': password})

        if response.status_code == 200:
            print(response.json())
            self.token = response.json()['data']['token']
            print('self.token = ' + self.token)
        else:
            print(f"Failed to get token. Status code: {response.status_code}")
            return None

    def upload_image(self, file_path):
        base_url = 'https://imgbed.sanyue.site/api/v1'
        upload_url = f'{base_url}/upload'

        headers = {'Authorization': f'Bearer {self.token}', 'Accept': 'application/json',
                   'Content-Type': 'multipart/form-data; charset=utf-8; boundary=+ Math.random().toString().substr(2))'}
        files = {'file': open(file_path, 'rb')}
        response = requests.post(upload_url, headers=headers, files=files)

        if response.status_code == 200:
            print("------------------")
            print(response.content)
            print("------------------")
            result = response.json()
            if result['status']:
                print(f"File uploaded successfully. Key: {result['data']['key']}")
                print(f"Access URL: {result['links']['url']}")
                return result['url']
            else:
                print(f"Upload failed. Error message: {result['message']}")
        else:
            print(f"Request failed with status code {response.status_code}")
