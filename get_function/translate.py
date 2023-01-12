import requests
import json
from loguru import logger


def get_your_translate(user_input, api_key):
    logger.error(f'User use the function get_your_translate')
    headers = {
        'X-API-Key': api_key,
        'Content-Type': 'text/xml; charset=utf-8; application/json',
        'Accept': 'application/json',
    }
    data = '{"texts": ["' + user_input + '"]  ,\n'  '"to": ["en"],\n        "from": "ru"\n    }'
    response = requests.post('https://api.lecto.ai/v1/translate/text', headers=headers, data=data.encode('utf-8'))
    var_json_object = json.loads(response.text)

    translation = var_json_object.get('translations')[0].get('translated')[0]
    return f'Твой перевод:\n\n{translation}'










