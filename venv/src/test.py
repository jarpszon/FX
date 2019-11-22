import OandaAPI as API
import datetime
from datetime import datetime


curr = 'EUR_USD'
strategyName = 'S1'
units = '2'
side = "SELL"
type = "MARKET"

"""
1. Plik strategyName_LastBarStartTime.txt z ostatnim barem w formacie %Y-%m-%d %H:%M:%S
"""

#check if current bar meet query criteria
currBarrStartTime,queryOK = API.GetPairHistForCheck(curr, count='12', gran = 'M15', query='Prev_1 > 0 ')
#print(str(currBarrStartTime) + " | " + str(queryOK))

#getting last full bast start time
with open("/usr/FX/OANDA/FX/venv/src/" + strategyName + '_LastBarStartTime.txt','r') as h:
    lastBarStartTime = h.readline()
if lastBarStartTime:
    lastBarStartTime = datetime.strptime(lastBarStartTime, "%Y-%m-%d %H:%M:%S" ) #  "%Y-%m-%dT%H:%M:%S.000000Z")
currBarrStartTime = datetime.strptime(currBarrStartTime, "%Y-%m-%dT%H:%M:%S.000000Z")
#print(str(lastBarStartTime) + ' | ' + str(currBarrStartTime) )

#check if current bar start time is > then last bar start time and if the query is met
if lastBarStartTime < currBarrStartTime:
    with open("/usr/FX/OANDA/FX/venv/src/" + strategyName + '_LastOrder.txt', 'w+') as h:
        lastOrderID = h.readline()
        # start
    with open("/usr/FX/OANDA/FX/venv/src/" + strategyName + '_spr.txt', 'a+') as h:
        h.write(str(lastOrderID))
        # stop
    if lastOrderID:
        a = API.CloseOpenTrades(str(int(lastOrderID)))
        # start
        with open("/usr/FX/OANDA/FX/venv/src/" + strategyName + '_spr.txt', 'a+') as h:
            h.write(str(str(a))
        # stop
        with open("/usr/FX/OANDA/FX/venv/src/" + strategyName + '_LastOrder.txt', 'w+') as h:
            h.write("")
        with open("/usr/FX/OANDA/FX/venv/src/" + strategyName + '_StratSummary.txt', 'a+') as h:
            h.write(str(a))

    if queryOK ==1:
        a=API.OpenMarketOrder(curr, units, side, type)
        with open("/usr/FX/OANDA/FX/venv/src/" + strategyName + '_LastOrder.txt', 'w+') as h:
            h.write(str(a))

    with open("/usr/FX/OANDA/FX/venv/src/" + strategyName + '_LastBarStartTime.txt','w+') as h:
        h.write(str(currBarrStartTime))


with open('/usr/FX/OANDA/FX/venv/src/logStrat1SA.txt','w+') as f:
    f.write(str(datetime.now()))



