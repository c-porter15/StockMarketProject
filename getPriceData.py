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
                        x['data']['attributes']['result']['%OvernightMovement(CloseVsOpen)'] = (float(histprices['historical'][y+1]['open'])  / float(dates['close'])) - 1
                        PriceData.append(x)
                        break
                y+=1
    return PriceData
            
def getKeyMetrics(PriceData, companies):
    for item in companies:
        metricprices = requests.get(f"https://financialmodelingprep.com/api/v3/company-key-metrics/{item}?period=quarter&from=2017-01-01&to=2020-02-02")
        metricprices = metricprices.json()
        for x in PriceData:
            date = x['data']['attributes']['filing']['period'][:-9]
            outerDate = str((datetime.datetime.strptime(date, '%Y-%m-%d') + datetime.timedelta(days = 10)).date())
            innerDate = str((datetime.datetime.strptime(date, '%Y-%m-%d') - datetime.timedelta(days = 10)).date())

            for obj in metricprices['metrics']:
                if innerDate < obj['date'] < outerDate:
                    if x['data']['attributes']['company']['ticker'] == item:
                        x['data']['attributes']['result']['Enterprise Value over EBITDA'] = float(obj['Enterprise Value over EBITDA'])
                        x['data']['attributes']['result']['EV to Operating cash flow'] = float(obj['EV to Operating cash flow'])
                        x['data']['attributes']['result']['EV to Free cash flow'] = float(obj['EV to Free cash flow'])
                        #x['data']['attributes']['result']['PE ratio'] = float(obj['PE ratio'][:-8])
                        break
    return PriceData

def getGrowthAndIncomeStatement(PriceData, companies):
    for item in companies:
        income_statement = requests.get(f"https://financialmodelingprep.com/api/v3/financials/income-statement/{item}?period=quarter")
        income_statement = income_statement.json()
        for x in PriceData:
            y = 0
            date = x['data']['attributes']['filing']['period'][:-9]

            for obj in income_statement['financials']:    
                if date == obj['date'] :
                    if x['data']['attributes']['company']['ticker'] == item:
                        x['data']['attributes']['result']['Revenue'] = float(obj['Revenue'])
                        x['data']['attributes']['result']['Net Income'] = float(obj['Net Income'])
                        try:
                            x['data']['attributes']['result']['%RevenueGrowth'] = (float(obj['Revenue']) / float(income_statement['financials'][y+1]['Revenue'])) - 1
                            x['data']['attributes']['result']['%Net Income Growth'] = (float(obj['Net Income']) / float(income_statement['financials'][y+1]['Net Income'])) - 1
                            x['data']['attributes']['result']['EPS Growth %'] = (float(obj['EPS Diluted']) / float(income_statement['financials'][y+1]['EPS Diluted'])) - 1
                        except: #expected error when calculating final iteration
                            x['data']['attributes']['result']['%RevenueGrowth'] = 0
                            x['data']['attributes']['result']['%Net Income Growth'] = 0 
                            x['data']['attributes']['result']['EPS Growth %'] = 0
                        break
                y+=1
    return PriceData

with open('StockMarketProject/consolidatedData.json', 'r') as infile:
    consolidatedData = json.load(infile)

PriceData = []
companies = ['msft', 'amzn', 'aapl', 'nflx', 'fb', 'jnj', 'v', 
            'pypl', 'pg', 'intc', 'amd', 'pfe', 'hon', 'sbux', 
            'ko', 'c', 'mcd', 'ma', 'txn', 'amgn']

PriceData = getHistoricalData(consolidatedData, PriceData, companies)
PriceData = getKeyMetrics(PriceData, companies)
PriceData = getGrowthAndIncomeStatement(PriceData, companies)

with open('StockMarketProject/consolidatedData.json', 'w') as outfile:
    json.dump(PriceData,outfile, indent=4)