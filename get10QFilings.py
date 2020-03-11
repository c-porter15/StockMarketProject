import http.client, urllib.request, urllib.parse, urllib.error, base64
import json
import time

n = 0

companies = ['MSFT', 'AMZN', 'AAPL', 'NFLX', 'FB', 'JNJ', 'V', 
            'PYPL', 'PG', 'INTC', 'AMD', 'PFE', 'HON', 'SBUX', 
            'KO', 'C', 'MCD', 'MA', 'TXN', 'AMGN']

headers = {
    # Request headers
    'Ocp-Apim-Subscription-Key': 'e97ef179ef2b4320bd8b7f5a35111f14',
}

formType = '10-Q'
conn = http.client.HTTPSConnection('services.last10k.com')
for i in range(len(companies)):
    rq_string1 = "/v1/company/"+companies[i]
    rq_string2 = "/balancesheet?formType="+formType
    for x in range(12):
        datafromfile = []
        fillingOrder = x
        rq_string3 = "&filingOrder=" + str(fillingOrder)
        conn.request("GET", rq_string1 + rq_string2 + rq_string3, "{body}", headers)
        response = conn.getresponse()
        dataString = response.read()    

        datafromfile.append(json.loads(dataString))

        with open('Code/PythonCode/StockMarketProject/data.json', 'a') as outfile:
            json.dump(datafromfile, outfile, indent=4)

        time.sleep(15)
        n+=1
        print(n)
        
conn.close()