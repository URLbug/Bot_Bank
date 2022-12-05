import json


opens_config = open('config.json')
opens_token = open('token.json')

config = json.load(opens_config)
token = json.load(opens_token)