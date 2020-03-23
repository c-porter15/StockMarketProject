import requests
import pandas as panda
import json, datetime

##https://financialmodelingprep.com/developer/docs/

with open('StockMarketProject/consolidatedData.json', 'r') as outfile:
    consolidatedData = json.load(outfile)

PriceData = []

companies = ['msft', 'amzn', 'aapl', 'nflx', 'fb', 'jnj', 'v', 
            'pypl', 'pg', 'intc', 'amd', 'pfe', 'hon', 'sbux', 
            'ko', 'c', 'mcd', 'ma', 'txn', 'amgn']

for item in companies:
    histprices = requests.get(f"https://financialmodelingprep.com/api/v3/historical-price-full/{item}?from=2017-01-01&to=2020-02-02")
    histprices = histprices.json()
        
    for x in consolidatedData:
        date1 = x['data']['attributes']['filing']['filingDate']
        y=0
        
        for dates in histprices['historical']:
            if date1 == dates['date']:
                if x['data']['attributes']['company']['ticker'] == item:
                    x['data']['attributes']['result']['Close'] = dates['close']
                    x['data']['attributes']['result']['%Change'] = dates['changePercent']
                    x['data']['attributes']['result']['NextDayOpen'] = histprices['historical'][y+1]['open']
                    x['data']['attributes']['result']['NextDay%Change'] = histprices['historical'][y+1]['changePercent']
                    x['data']['attributes']['result']['%OvernightMovement(CloseVsOpen)'] = (((float(histprices['historical'][y+1]['open']) - float(dates['close']))/float(dates['close'])) * 100).__round__(2)
                    PriceData.append(x)
                    break
            y+=1
            
with open('StockMarketProject/consolidatedData.json', 'w') as outfile3:
    json.dump(PriceData,outfile3, indent=4)