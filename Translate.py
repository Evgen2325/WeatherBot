import requests

apiKey = ('6QH0KNY-F9QMSFK-QG52CWT-EZ54JYS')
headers = {
    'X-API-Key': apiKey,
    'Content-Type': 'text/xml; charset=utf-8; application/json',
    'Accept': 'application/json',
}
user_input = input("Введите текс ")
data = '{"texts": ["' + user_input + '"]  ,\n'  '"to": ["ru"],\n        "from": "en"\n    }'

response = requests.post('https://api.lecto.ai/v1/translate/text', headers=headers, data=data.encode('utf-8'))

print("Json Response ", response.json())
result_text = response.raw()
translate = result_text['translations']['translated']
print(f'Твой перевод {translate}')







