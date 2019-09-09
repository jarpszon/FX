import OandaAPI as api
from datetime import datetime
from datetime import timedelta

#api.GetPairHist("EUR_USD","","","M15","2")
#api.GetAccountInfo()
"""
a = api.GetCurrPrice("GBP_USD")
print(a['prices'][0]['instrument'])
print(a['prices'][0]['time'])
print(a['prices'][0]['bid'])
print(a['prices'][0]['ask'])

"""

# GENERATE HISTORY DATA

currListMajor = ['EUR_USD', 'GBP_USD','USD_CAD','USD_CHF','USD_JPY']

for curr in currListMajor:
    with open("C:/Users/jpszonczak/Documents/Inne/Prywata\FX/OANDA/" + curr + "15min.txt", "a+") as h:
        h.write("<TICKER>,<DATETIME>,<HOUR>,<OPEN>,<HIGH>,<LOW>,<CLOSE>,<VOL>")
        h.write('\n')
    startdate = "2018-12-31"
    startdate = datetime.strptime(startdate, "%Y-%m-%d")
    for x in range(243):
        startdate = startdate + timedelta(days=1)
        enddate = startdate + timedelta(days=1)
        a = str(startdate.strftime("%Y-%m-%d"))  + "T00%3A00%3A00Z"
        b = str(enddate.strftime("%Y-%m-%d")) + "T00%3A00%3A00Z"
        api.GetPairHist(curr, a, b, "M15",
                    file="C:/Users/jpszonczak/Documents/Inne/Prywata\FX/OANDA/" + curr + "15min.txt")




