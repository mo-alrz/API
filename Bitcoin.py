import requests

r = requests.get('https://api.coinbase.com/v2/prices/buy?cuurency=USD')
price = r.json()["data"]["amount"]
print(f'The current Bitcoin price is : {price} $')
