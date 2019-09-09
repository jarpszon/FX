import pandas as pd
from openpyxl import load_workbook
import itertools as it

currListMajor = ['EUR_USD', 'GBP_USD','USD_CAD','USD_CHF','USD_JPY']

for curr in currListMajor:
    path = "C:/Users/jpszonczak/Documents/Inne/Prywata/FX/OANDA/" + curr + "15min.txt"

    df = pd.read_csv(path, sep=",", header=0)

    df['Move']    = df['CLOSE'] - df['OPEN']
    df['Prev_1']  = df['CLOSE'].shift(1) - df['OPEN'].shift(1)
    df['Prev_2']  = df['CLOSE'].shift(2) - df['OPEN'].shift(2)
    df['Prev_3']  = df['CLOSE'].shift(3) - df['OPEN'].shift(3)
    df['Prev_4']  = df['CLOSE'].shift(4) - df['OPEN'].shift(4)
    df['Prev_5']  = df['CLOSE'].shift(5) - df['OPEN'].shift(5)
    df['Prev_6']  = df['CLOSE'].shift(6) - df['OPEN'].shift(6)
    df['Prev_7']  = df['CLOSE'].shift(7) - df['OPEN'].shift(7)
    df['Prev_8']  = df['CLOSE'].shift(8) - df['OPEN'].shift(8)
    df['Prev_9']  = df['CLOSE'].shift(9) - df['OPEN'].shift(9)
    df['Prev_10'] = df['CLOSE'].shift(10) - df['OPEN'].shift(10)


    with open("C:/Users/jpszonczak/Documents/Inne/Prywata/FX/OANDA/wynik.txt", "a+") as f:
        for x in range(10):
        #for x in range(3):
            perm = it.product('><', repeat=x+2)
            for i in list(perm):
                query = ''
                for j in range(len(i)):
                    m = lambda r: 'Move' if j == 0 else ('Prev_' + str(j) )
                    n = lambda t: 'and ' if j < len(i)-1 else ''
                    #print( m(0) + ' ' + str(i[j]) + ' 0 ' + n(0), end='')
                    query = (query + m(0) + ' ' + str(i[j]) + ' 0 ' + n(0))
                #print('')
                #print(query)
                #print(query.replace('`Move` > 0 and ','').replace('`Move` < 0 and ',''))

                s = len(df.query(query))
                #print(s)

                query1 = query.replace('Move > 0 and ', '').replace('Move < 0 and ', '')
                #print(s , end=' | ')
                t = len(df.query(query1))
                if t > 0:
                    ratio = '{: .2f}'.format(s/t*100)
                else:
                    ratio = 0
                #print(t, end=' | ')
                #print(ratio)

                if t != 0:
                    f.write(curr + ' | ' + 'Ratio ' + str(ratio) +   ' | Sukces: ' + str(s)  + ' | ' +  ' Total ' + str(t) + ' | ' + 'Param: ' + query)
                    f.write('\n')

