import yahoo_finance
import datetime

date_format = "%Y-%m-%d"

def backtest (ticker = "HD", start = "2006-10-01", end = "2015-10-01", duration = 50):
    global date_format
    stake = yahoo_finance.Share(ticker)
    stake.refresh()
    historical_data = stake.get_historical(start, end)
    i = len(historical_data) - 1
    totalGains = 0
    haveStock = False
    origStockPrice = None
    while i - duration + 1 >= 0:
        durationData = historical_data[i - duration + 1: i + 1]
        sum = 0
        for singleData in durationData:
            sum += float(singleData['Close'])
        avg = sum / duration
        if avg > float(durationData[0]['Close']) and haveStock:
            # sell stock
            haveStock = False
            totalGains += float(durationData[0]['Close']) - origStockPrice

        elif avg < float(durationData[0]['Close']) and (not haveStock):
            #buy stock
            haveStock = True
            origStockPrice = float(durationData[0]['Close'])
        i -= duration
    return totalGains / float(historical_data[-1]['Close'])
        # avg = new_avg
    # print historical_data[0]
    # preDate = datetime.datetime.strptime(historical_data[0]['Date'], date_format).date().strftime(date_format)
    # print preDate
    # print (preDate == end)
    # print datetime.datetime.strptime(end, "%Y-%m-%d").date() + datetime.timedelta(days = 20)
    
def sectortest (startdates = ["2003-01-01"], enddates =["2009-01-01"], durations =[100], file ="test2"):
    with open (file, "w") as f:
        f.write ("")

def realbacktest (ticker = "HD", start = "2006-10-01", end = "2015-10-01", duration = 50, commission = 2, file = "test3"):
    with open (file, "w") as f:
        f.write ("")

print backtest('AAPL', "2014-01-01", "2015-10-23", 20)