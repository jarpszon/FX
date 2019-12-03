import OandaAPI as API
import datetime
from datetime import datetime


curr = 'EUR_USD'
strategyName = 'S1'
units = '2'
side = "SELL"
type = "MARKET"


file_path = "/usr/FX/OANDA/FX/venv/src/"
#file_path = ''
"""
1. Plik strategyName_LastBarStartTime.txt z ostatnim barem w formacie %Y-%m-%d %H:%M:%S
"""

#check if current bar meet query criteria
currBarrStartTime,queryOK = API.GetPairHistForCheck(curr, count='12', gran = 'M15', query='Prev_1 > 0 ')
#print(str(currBarrStartTime) + " | " + str(queryOK))

#getting last full bast start time
with open(file_path + strategyName + '_LastBarStartTime.txt','r') as h:
    lastBarStartTime = h.readline()

if lastBarStartTime:
    lastBarStartTime = datetime.strptime(lastBarStartTime, "%Y-%m-%d %H:%M:%S" ) #  "%Y-%m-%dT%H:%M:%S.000000Z")

currBarrStartTime = datetime.strptime(currBarrStartTime, "%Y-%m-%dT%H:%M:%S.000000Z")
print(str(lastBarStartTime) + ' | ' + str(currBarrStartTime) )

#check if current bar start time is > then last bar start time and if the query is met
if lastBarStartTime < currBarrStartTime:
    with open(file_path + strategyName + '_LastOrder.txt', 'r+') as h:
        lastOrderID = h.readline()
    print('Last order from the file: ' + lastOrderID)
    if lastOrderID:
        a = API.CloseOpenTrades(str(int(lastOrderID) + 1))
        print('a = ' + str(a))
        with open(file_path + strategyName + '_LastOrder.txt', 'w+') as h:
            h.write("")
        with open(file_path + strategyName + '_StratSummary.txt', 'a+') as h:
            h.write(str(a))

    if queryOK ==1:
        a=API.OpenMarketOrder(curr, units, side, type)
        with open(file_path + strategyName + '_LastOrder.txt', 'w+') as h:
            h.write(str(a))

    with open(file_path + strategyName + '_LastBarStartTime.txt','w+') as h:
        h.write(str(currBarrStartTime))
