import yaml
import json
import requests as rq
import datetime as dt
import OandaAPI as API

with open("config.yaml", 'r') as stream:
    data_loaded = yaml.safe_load(stream)

token=data_loaded['token']
user=data_loaded['username']
host=data_loaded['host']


def OpenMarketOrder(pair, units, side, type,ts):
    url = host + "/v3/accounts/101-004-12033863-001/orders"
    payload =  "{\"order\": {\"instrument\": \"" + pair +  "\", \"units\": "  + units + ", \"side\": \"" + side + "\", \"type\": \"" + type + "\", \"trailingstop\": \"" + ts + "\"}}"
    print(payload)
    head = {'Content-Type': "application/json", 'Authorization': 'Bearer 36d05c504600ee53cbaebd2d7fd872f6-ec6ea1868a87be65621c6c23ba0e9fe1'}
    response = rq.post(url=url, data=payload, headers=head)
    b=response.json()
    #print(b["orderCreateTransaction"]["id"] + " | " + b["orderCreateTransaction"]["instrument"])
    return b["orderCreateTransaction"]["id"]

OpenMarketOrder("EUR_USD","2", "sell", "MARKET","1000")
"""
#API.GetOpenTradesId()
url = host + "/v3/accounts/101-004-12033863-001/openTrades"
head = {'Content-Type': "application/json",
        'Authorization': 'Bearer 36d05c504600ee53cbaebd2d7fd872f6-ec6ea1868a87be65621c6c23ba0e9fe1'}
response = rq.get(url, headers=head)
res_json = response.json()
print(res_json)
"""
for x in API.GetOpenTradesId():
    API.CloseOpenTrades(x)
API.GetOpenTradesId()
"""

