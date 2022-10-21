import requests
import json

apiKey = ('6QH0KNY-F9QMSFK-QG52CWT-EZ54JYS')
headers = {
    'X-API-Key': apiKey,
    'Content-Type': 'text/xml; charset=utf-8; application/json',
    'Accept': 'application/json',
}
user_input = input("Введите текс ")
data = '{"texts": ["' + user_input + '"]  ,\n'  '"to": ["ru"],\n        "from": "en"\n    }'
response = requests.post('https://api.lecto.ai/v1/translate/text', headers=headers, data=data.encode('utf-8'))
var_json_object = json.loads(response.text)

translation = var_json_object.get('translations')[0].get('translated')[0]
print(f'Твой перевод:\n\n{translation}')

def get_tranlation_from_raw(raw_string):
    result = ''
    start_index = raw_string.find('translated')


    return result






