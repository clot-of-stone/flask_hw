import requests

res = requests.get('http://127.0.0.1:5001')
print(res.status_code)
print(res.text)
