import requests

x = requests.get('https://mcdn-a.akamaihd.net/br/hf/7t/')

print(x.content)

