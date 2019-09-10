import yaml
import json
import requests as rq
import datetime as dt
import pandas as pd

with open("config.yaml", 'r') as stream:
    data_loaded = yaml.safe_load(stream)

token=data_loaded['token']
user=data_loaded['username']
host=data_loaded['host']


#def OpenMarketOrder(pair, units,side):

def OANDAServiceCheck():
#nie działa
    url="http://api-status.oanda.com/api/v1/services"
    head = {'Content-Type': "application/json", 'Authorization': 'Bearer 36d05c504600ee53cbaebd2d7fd872f6-ec6ea1868a87be65621c6c23ba0e9fe1'}
    response = rq.get(url) #--( , headers=head)
    res_json = response.json()
    print(res_json)
    print(response)

def CloseOpenTrades(TradeId):
    url = host + "/v3/accounts/101-004-12033863-001/trades/" + str(TradeId) + "/close"
    #print(url)
    head = {'Content-Type': "application/json", 'Authorization': 'Bearer 36d05c504600ee53cbaebd2d7fd872f6-ec6ea1868a87be65621c6c23ba0e9fe1'}
    response = rq.put(url, headers=head)
    #print(response)
    res_json = response.json()
    return res_json
    #print(res_json)


def GetOpenTradesId():
    url = host + "/v3/accounts/101-004-12033863-001/openTrades"
    head = {'Content-Type': "application/json", 'Authorization': 'Bearer 36d05c504600ee53cbaebd2d7fd872f6-ec6ea1868a87be65621c6c23ba0e9fe1'}
    response = rq.get(url, headers=head)
    res_json = response.json()
    a = []
    for x in range(len(res_json['trades'])):
        a.append(res_json['trades'][x]['id'])
        #print(res_json['trades'][x]['id'])
    print(a)
    return a

def OpenMarketOrder(pair, units, side, type):
    url = host + "/v3/accounts/101-004-12033863-001/orders"
    payload =  "{\"order\": {\"instrument\": \"" + pair +  "\", \"units\": "  + units + ", \"side\": \"" + side + "\", \"type\": \"" + type + "\"}}"
    #print(payload)
    head = {'Content-Type': "application/json", 'Authorization': 'Bearer 36d05c504600ee53cbaebd2d7fd872f6-ec6ea1868a87be65621c6c23ba0e9fe1'}
    response = rq.post(url=url, data=payload, headers=head)
    b=response.json()
    #print(b["orderCreateTransaction"]["id"] + " | " + b["orderCreateTransaction"]["instrument"])
    #print(b)
    return b["orderFillTransaction"]["tradeOpened"]["tradeID"]

def GetCurrPrice(pair):
    url = host + "/v1/prices?instruments=" + pair
    head = {'Authorization': 'Bearer ' + token}
    response = rq.get(url, headers=head)
    res_json = response.json()
    return(res_json)
    """
    print(res_json)
    print(res_json['prices'][0]['instrument'])
    print(res_json['prices'][0]['time'])
    print(res_json['prices'][0]['bid'])
    print(res_json['prices'][0]['ask'])
    """

def GetAccountInfo():
    url = host + '/v3/accounts/101-004-12033863-001'
    head = {'Authorization': 'Bearer ' + token}
    response = rq.get(url, headers=head)
    res_json = response.json()
    return res_json
    #print(response.content.decode())



def GetPairHist(pair, startDate, endDate,gran, count = '', file = ''):
    #url = "https://" + host + "/v1/candles?instrument=" + pair + "&count=" + count + "&candleFormat=midpoint&granularity=" + gran + "&dailyAlignment=0&alignmentTimezone=America%2FNew_York"
    if count != '':
        url = host + "/v1/candles?instrument=" + pair + "&count=" + count + "&candleFormat=midpoint&granularity=" + gran + "&dailyAlignment=0&alignmentTimezone=America%2FNew_York"
    else:
        url = host + "/v1/candles?instrument=" + pair + "&start=" + startDate + "&end=" + endDate +  "&candleFormat=midpoint&granularity=" + gran + "&dailyAlignment=0&alignmentTimezone=America%2FNew_York"
    print(url)

# API request
    head = {'Authorization': 'Bearer ' + token}
    response = rq.get(url, headers=head)
    print(response.status_code)
    if response.status_code == 200:
        res_json = response.json()
        with open(file, "a+") as f:
            for x in range(len(res_json['candles'])):
                """
                print( pair
                        + ',' + str(dt.datetime.strptime(res_json['candles'][x]['time'],'%Y-%m-%dT%H:%M:%S.%fZ'))
                        + ',' + str(dt.datetime.strptime(res_json['candles'][x]['time'],'%Y-%m-%dT%H:%M:%S.%fZ').hour)
                        + ',' + str(res_json['candles'][x]['openMid'])
                        + ',' + str(res_json['candles'][x]['highMid'])
                        + ',' + str(res_json['candles'][x]['lowMid'])
                        + ',' + str(res_json['candles'][x]['closeMid'])
                        + ',' + str(res_json['candles'][x]['volume'])
                        )
                """
                f.write( pair
                        + ',' + str(dt.datetime.strptime(res_json['candles'][x]['time'],'%Y-%m-%dT%H:%M:%S.%fZ'))
                        + ',' + str(dt.datetime.strptime(res_json['candles'][x]['time'],'%Y-%m-%dT%H:%M:%S.%fZ').hour)
                        + ',' + str(res_json['candles'][x]['openMid'])
                        + ',' + str(res_json['candles'][x]['highMid'])
                        + ',' + str(res_json['candles'][x]['lowMid'])
                        + ',' + str(res_json['candles'][x]['closeMid'])
                        + ',' + str(res_json['candles'][x]['volume'])
                        )
                f.write('\n')


# returns start time of last candle and 1 if it satisfies the query and 0 if not
def GetPairHistForCheck(pair, count = '', gran = '', query = ''):
    url = host + "/v1/candles?instrument=" + pair + "&count=" + count + "&candleFormat=midpoint&granularity=" + gran + "&dailyAlignment=0&alignmentTimezone=America%2FNew_York"
    #print(url)

# API request
    head = {'Authorization': 'Bearer ' + token}
    response = rq.get(url, headers=head)
    #print(response.status_code)
    if response.status_code == 200:
        res_json = response.json()
        df = pd.io.json.json_normalize(res_json['candles'])
        #print(df)
        #print(df.loc[df['complete'] == 1])

        df = df.loc[df['complete'] == 1]
        df['Move']    = df['closeMid'] - df['openMid']
        df['Prev_1']  = df['closeMid'].shift(1) - df['openMid'].shift(1)
        df['Prev_2']  = df['closeMid'].shift(2) - df['openMid'].shift(2)
        df['Prev_3']  = df['closeMid'].shift(3) - df['openMid'].shift(3)
        df['Prev_4']  = df['closeMid'].shift(4) - df['openMid'].shift(4)
        df['Prev_5']  = df['closeMid'].shift(5) - df['openMid'].shift(5)
        df['Prev_6']  = df['closeMid'].shift(6) - df['openMid'].shift(6)
        df['Prev_7']  = df['closeMid'].shift(7) - df['openMid'].shift(7)
        df['Prev_8']  = df['closeMid'].shift(8) - df['openMid'].shift(8)
        df['Prev_9']  = df['closeMid'].shift(9) - df['openMid'].shift(9)
        df['Prev_10'] = df['closeMid'].shift(10) - df['openMid'].shift(10)
        #print(len(df))
        #print(df.tail(1))
        #print(df.tail(1)['time'])
        #print(len(df.tail(1).query(query)) )
        #print(df.query(query))

        return df.tail(1).iloc[0]['time'], len(df.tail(1).query(query))


###################################################################################################################################################################

if __name__ == '__main__':
    #GetPairHist("EUR_USD","","","M15","10")
    #GetPairHist("EUR_USD","2019-08-26T00%3A00%3A00Z","2019-08-27T00%3A00%3A00Z","M15",file="C:/Users/jpszonczak/Desktop/EURUSD15min.txt")
    #GetPairHist("EUR_USD", "2019-08-27T00%3A00%3A00Z", "2019-08-28T00%3A00%3A00Z", "M15",file="C:/Users/jpszonczak/Desktop/EURUSD15min.txt")
    #print(GetAccountInfo())
    #print(GetCurrPrice("EUR_USD"))
    #OpenMarketOrder()
    #GetOpenTradesId()
    #CloseOpenTrades()
    #for x in GetOpenTradesId():
    #a = CloseOpenTrades(103)

    GetOpenTradesId()
    #OANDAServiceCheck()
    #a,b = GetPairHistForCheck('EUR_USD', count='12', gran = 'M15', query='Prev_9 < 0 and Prev_10 < 0')
    #print(str(a) + " | " + str(b))
    """
    curr = 'EUR_USD'
    strategyName = 'S1'
    units = '2'
    side = "SELL"
    type = "MARKET"
    newOrderID = OpenMarketOrder(curr, units, side, type)
    print(newOrderID)
    """

