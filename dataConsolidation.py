import json, csv, datetime

##Converted table of CSV data to JSON Objects
##Output: JSON objects in EPSdata.json
def csv2json(): 
    columnNames = ("Ticker", "Date", "EPS_Estimate", "EPS", "EPS_Surprise")

    jsonFile = open('Code/PythonCode/EPSdata.json', 'w')

    with open('Code/PythonCode/data.csv') as csvFile:
        csvReader = csv.DictReader(csvFile, columnNames)

        for rows in csvReader:
            json.dump(rows,jsonFile, indent=4)
            jsonFile.write('\n')


#The following code snippet crossreferenced two json files. If both json files had the same date and ticker
#added the the EPS object elements to the respective 10Q object then adding the object to consolidatedData.json

with open('Code/PythonCode/StockMarketProject/10Qdata.json', 'r') as outfile:
    filingData = json.load(outfile)

with open('Code/PythonCode/StockMarketProject/epsData.json', 'r') as outfile2:
    epsData = json.load(outfile2)
    
newdata = []

for obj in filingData:
    date = obj['data']['attributes']['filing']['filingDate'][:-9]
    ticker = obj['data']['attributes']['company']['ticker'].upper()

    outerDate = str((datetime.datetime.strptime(date, '%Y-%m-%d') + datetime.timedelta(days = 30)).date())
    innerDate = str((datetime.datetime.strptime(date, '%Y-%m-%d') - datetime.timedelta(days = 30)).date())

    for eps in epsData:
        temp = eps['Date']
        eps['Date'] = eps['Date'][:-15].lstrip()
        eps['Ticker'] = eps['Ticker'].strip()

        if innerDate < eps['Date'] < outerDate:
            if ticker == eps['Ticker']:
                obj['data']['attributes']['result']['EPS'] = float(eps['EPS'])
                obj['data']['attributes']['result']['EPS_Estimate'] = float(eps['EPS_Estimate'])
                obj['data']['attributes']['result']['EPS_Surprise'] = float(eps['EPS_Surprise'])
                newdata.append(obj)
        eps['Date'] = temp

with open('Code/PythonCode/StockMarketProject/consolidatedData.json', 'a') as outfile3:
    json.dump(newdata,outfile3, indent=4)