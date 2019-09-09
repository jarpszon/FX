import yaml
import json
import requests as rq
import datetime as dt

with open("config.yaml", 'r') as stream:
    data_loaded = yaml.safe_load(stream)

token=data_loaded['token']
user=data_loaded['username']
host=data_loaded['host']

def GetAccountInfo():
    url = 'https://' + host + '/v3/accounts/101-004-12033863-001'
    url = 'https://' + host + '/v3/accounts'
    print(url)
    head = {'Authorization': 'Bearer ' + token}
    response = rq.get(url, headers=head)
    res_json = response.json()
    print(response.content.decode())
    print(token)
    print(head)

def GetPairHist(pair, startDate, endDate,gran, count):
    url = "https://" + host + "/v1/candles?instrument=" + pair + "&count=" + count + "&candleFormat=midpoint&granularity=" + gran + "&dailyAlignment=0&alignmentTimezone=America%2FNew_York"
    #url = "https://api-fxtrade.oanda.com/v1/candles?instrument=EUR_USD&count=10&candleFormat=midpoint&granularity=M15&dailyAlignment=0&alignmentTimezone=America%2FNew_York"

#    print(url)

# API request
    head = {'Authorization': 'Bearer ' + token}
    response = rq.get(url, headers=head)
    res_json = response.json()
    for x in range(len(res_json['candles'])):
        print( str(dt.datetime.strptime(res_json['candles'][x]['time'],'%Y-%m-%dT%H:%M:%S.%fZ'))
                + ',' + str(dt.datetime.strptime(res_json['candles'][x]['time'],'%Y-%m-%dT%H:%M:%S.%fZ').hour)
                + ',' + str(res_json['candles'][x]['openMid'])
                + ',' + str(res_json['candles'][x]['highMid'])
                + ',' + str(res_json['candles'][x]['lowMid'])
                + ',' + str(res_json['candles'][x]['closeMid'])
                + ',' + str(res_json['candles'][x]['volume'])
                )

if __name__ == '__main__':
    #GetPairHist("EUR_USD","","","M15","10")
    GetAccountInfo()


""""teraerasr"""

