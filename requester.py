import requests

url = 'http://10.250.4.94:5000/api/pos'
payload = {'key': 'value'}

headers = {'Content-Type': 'application/json'}
response = requests.post(url, json=payload, headers=headers)

print(response.json())