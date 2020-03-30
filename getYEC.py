import datetime
import xlsxwriter
from yahoo_earnings_calendar import YahooEarningsCalendar

companies = ['MSFT', 'AMZN', 'AAPL', 'NFLX', 'FB', 'JNJ', 'V', 
            'PYPL', 'PG', 'INTC', 'AMD', 'PFE', 'HON', 'SBUX', 
            'KO', 'C', 'MCD', 'MA', 'TXN', 'AMGN']

beginDates = ["Jan 7", "Oct 7", "Jul 7", "Apr 7"]

endDates = ["Feb 10", "Nov 10", "Aug 10", "May 7"]

###############################################
date_from = datetime.datetime.strptime(
    'Jan 20 2020 9:30AM', '%b %d %Y %I:%M%p')
date_to = datetime.datetime.strptime(
    'Jan 31 2020 4:00PM', '%b %d %Y %I:%M%p')

yec = YahooEarningsCalendar()
newCalendar = yec.earnings_between(date_from, date_to)

for x in newCalendar:
    if(x['ticker'] in companies):
        print(x['ticker'], ",", x['startdatetime'], ",", x['epsestimate'], ",", x['epsactual'], ",", x['epssurprisepct'])

###############################################
for i in range(len(beginDates)):
    for n in range(7,10):
        date_from = datetime.datetime.strptime(
            '{0} 201{1} 9:30AM'.format(beginDates[i], n), '%b %d %Y %I:%M%p')
        date_to = datetime.datetime.strptime(
            '{0} 201{1} 4:00PM'.format(endDates[i], n), '%b %d %Y %I:%M%p')

        newCalendar = yec.earnings_between(date_from, date_to)

        for x in newCalendar:
            if(x['ticker'] in companies):
                print(x['ticker'], ",", x['startdatetime'], ",", x['epsestimate'], ",", x['epsactual'], ",", x['epssurprisepct'])

