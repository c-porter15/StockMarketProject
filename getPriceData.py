import requests
import json, datetime

##https://financialmodelingprep.com/developer/docs/

def getHistoricalData(consolidatedData, PriceData, companies):
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
    return PriceData
            
def getKeyMetrics(consolidatedData, PriceData, companies):
    for item in companies:
        metricprices = requests.get(f"https://financialmodelingprep.com/api/v3/company-key-metrics/{item}?period=quarter&from=2017-01-01&to=2020-02-02")
        metricprices = metricprices.json()
        for x in consolidatedData:
            date = x['data']['attributes']['filing']['period'][:-9]
            outerDate = str((datetime.datetime.strptime(date, '%Y-%m-%d') + datetime.timedelta(days = 10)).date())
            innerDate = str((datetime.datetime.strptime(date, '%Y-%m-%d') - datetime.timedelta(days = 10)).date())

            for obj in metricprices['metrics']:
                if innerDate < obj['date'] < outerDate:
                    if x['data']['attributes']['company']['ticker'] == item:
                        x['data']['attributes']['result']['Enterprise Value over EBITDA'] = float(obj['Enterprise Value over EBITDA'])
                        x['data']['attributes']['result']['EV to Operating cash flow'] = float(obj['EV to Operating cash flow'])
                        x['data']['attributes']['result']['EV to Free cash flow'] = float(obj['EV to Free cash flow'])
                        #x['data']['attributes']['result']['PE ratio'] = float(x['data']['attributes']['result']['PE ratio'][:-8])
                        PriceData.append(x)
                        break
    return PriceData

def getIncomeStatement(consolidatedData, PriceData, companies):
    for item in companies:
        income_statement = requests.get(f"https://financialmodelingprep.com/api/v3/financials/income-statement/{item}?period=quarter")
        income_statement = income_statement.json()
        for x in consolidatedData:
            date = x['data']['attributes']['filing']['period'][:-9]
            outerDate = str((datetime.datetime.strptime(date, '%Y-%m-%d') + datetime.timedelta(days = 10)).date())
            innerDate = str((datetime.datetime.strptime(date, '%Y-%m-%d') - datetime.timedelta(days = 10)).date())
            for obj in income_statement['financials']:
                if innerDate < obj['date'] < outerDate:
                    if x['data']['attributes']['company']['ticker'] == item:
                        x['data']['attributes']['result']['Revenue'] = float(obj['Revenue'])
                        x['data']['attributes']['result']['Net Income'] = float(obj['Net Income'])
                        PriceData.append(x)
                        break
    return PriceData

with open('StockMarketProject/consolidatedData.json', 'r') as infile:
    consolidatedData = json.load(infile)

PriceData = []
companies = ['msft', 'amzn', 'aapl', 'nflx', 'fb', 'jnj', 'v', 
            'pypl', 'pg', 'intc', 'amd', 'pfe', 'hon', 'sbux', 
            'ko', 'c', 'mcd', 'ma', 'txn', 'amgn']
PriceData = getKeyMetrics(consolidatedData, PriceData, companies)
PriceData = getHistoricalData(consolidatedData, PriceData, companies)
PriceData = getIncomeStatement(consolidatedData, PriceData, companies)

with open('StockMarketProject/consolidatedData.json', 'w') as outfile:
    json.dump(PriceData,outfile, indent=4)