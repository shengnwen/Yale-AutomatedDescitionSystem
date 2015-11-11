import yahoo_finance
import datetime

date_format = "%Y-%m-%d"
sector_info = None
# best_avg_period = None
# best_avg_duration = None
# max_avg_period = None
# max_avg_duration = None

def backtest (ticker = "HD", start = "2006-10-01", end = "2015-10-01", duration = 50):
    # global max_avg_period, max_avg_duration
    global sector_info
    stake = yahoo_finance.Share(ticker)
    stake.refresh()
    historical_data = stake.get_historical(start, end)
    if len(historical_data) == 0 or len(historical_data) < duration:
        return
    historical_data = historical_data[::-1]
    # print historical_data[0]
    # for data in historical_data:
    #     print data['Date'] + ":" + data['Adj_Close']
    i = 0
    total_gains = 0
    have_stock = False
    old_price = None
    total_sum = 0
    for single_day in historical_data:
        total_sum += float(single_day['Adj_Close'])
    while i + duration <= len(historical_data):
        sum = 0
        for single_day in historical_data[i: i+duration]:
            sum += float(single_day['Adj_Close'])
        avg = sum / duration
        # if max_duration is None or max_avg_duration[2] < avg:
        #     max_avg_duration = ["avg-duration", duration, avg]
        new_price = float(historical_data[i+duration - 1]['Adj_Close'])
        if avg > new_price and have_stock:
            # sell stock
            have_stock = False
            total_gains += new_price - old_price
        elif avg < new_price and (not have_stock):
            have_stock = True
            old_price = new_price
        i += 1
    # sector_info = [ticker, start, end, str(duration), str((float(historical_data[-1]['Adj_Close']) - float(historical_data[0]['Adj_Close']))/float(historical_data[0]['Adj_Close']))]
    sector_info = [ticker, start, end, str(duration), str(total_gains / float(historical_data[0]['Adj_Close']))]
    # print total_gains
    # print float(historical_data[-1]['Adj_Close']) - float(historical_data[0]['Adj_Close'])
    return total_gains / float(historical_data[0]['Adj_Close'])

    
def sectortest (startdates = ["2003-01-01"], enddates =["2009-01-01"], durations =[100], file ="test2"):
    sectors = ["XLY", "XLP", "XLE", "XLFS", "XLF", "XLV", "XLI", "XLB", "XLRE", "XLK", "XLU"]
    global sector_info
    best = []
    worst = []
    max = None
    min = None
    backtest_result = []
    for sector in sectors:
        sector_result = []
        for i in range(0, len(startdates)):
            start = startdates[i]
            end = enddates[i]
            period_result = []
            for duration in durations:
                val = backtest(sector, start, end, duration)
                period_result.append(val)
                if val is None:
                    # print "val is none here"
                    continue
                # print val
                if max is None or max < val:
                    best = ['best']
                    max = val
                    for ele in sector_info:
                        best.append(ele)
                if min is None or min > val:
                    min = val
                    worst = ['worst']
                    for ele in sector_info:
                        worst.append(ele)
            sector_result.append(period_result)
        backtest_result.append(sector_result)
    # print backtest_result
    # print ' '.join(best)
    # print max
    # print " ".join(worst)
    # print min
    # best avg period
    max_avg_period = None
    max_avg = None
    for i in range(0, len(startdates)):
        period_sum = 0
        count = 0
        for sector_index in range(0, len(sectors)):
            for duration_index in range(0,len(durations)):
                if backtest_result[sector_index][i][duration_index] is None:
                    continue
                period_sum += backtest_result[sector_index][i][duration_index]
                count += 1
        avg_period = period_sum / count
        if max_avg is None or max_avg < avg_period:
            max_avg = avg_period
            max_avg_period = ["avg-period", startdates[i], enddates[i], str(avg_period)]
    # print ' '.join(max_avg_period)
    max_avg_duration = None
    max_avg = None
    for i in range(0, len(durations)):
        duration_sum = 0
        count = 0
        for sector_index in range(0, len(sectors)):
            for period_index in range(0,len(startdates)):
                if backtest_result[sector_index][period_index][i] is None:
                    continue
                duration_sum += backtest_result[sector_index][period_index][i]
                count += 1
        avg_duration = duration_sum / count
        if max_avg is None or max_avg < avg_duration:
            max_avg = avg_duration
            max_avg_duration = ['avg-duration', str(durations[i]), str(avg_duration)]
    # print ' '.join(max_avg_duration)

    with open (file, "w") as f:
        result = ' '.join(best) + "\n"
        result += ' '.join(worst) + "\n"
        result += " ".join(max_avg_period) + "\n"
        result += " ".join(max_avg_duration) + "\n"
        f.write (result)

def realbacktest (ticker = "HD", start = "2006-10-01", end = "2015-10-01", duration = 50, commission = 2, file = "test3"):
    commission_cost = commission * 0.0001
    # print commission_cost
    stake = yahoo_finance.Share(ticker)
    stake.refresh()
    historical_data = stake.get_historical(start, end)
    if len(historical_data) == 0 or len(historical_data) < duration:
        return
    historical_data = historical_data[::-1]
    i = 0
    total_gains = 0
    have_stock = False
    old_price = None
    initial_price = None
    total_sum = 0
    for single_day in historical_data:
        total_sum += float(single_day['Adj_Close'])
    while i + duration <= len(historical_data):
        sum = 0
        for single_day in historical_data[i: i+duration]:
            sum += float(single_day['Adj_Close'])
        avg = sum / duration
        # if max_duration is None or max_avg_duration[2] < avg:
        #     max_avg_duration = ["avg-duration", duration, avg]
        new_price = float(historical_data[i+duration - 1]['Adj_Close'])
        if avg > new_price and have_stock:
            # sell stock
            have_stock = False
            total_gains += new_price - old_price - commission_cost * new_price
        elif avg < new_price and (not have_stock):
            # buy stock
            if initial_price is None:
                initial_price = avg
            have_stock = True
            old_price = new_price
            total_gains -= commission_cost * new_price
        i += 1
    result_str = ""
    #net return
    result_str += str(round(total_gains / initial_price, 3)) + " net return, moving average."
    buy_hold_gain = float(historical_data[-1]['Adj_Close']) - float(historical_data[0]['Adj_Close'])
    result_str += "\n"
    #buy and hold return
    result_str += str(round(buy_hold_gain / float(historical_data[0]['Adj_Close']), 3)) + " buy and hold return."
    # total buy and hold return
    result_str += "\n"
    total_buy_hold_gain = buy_hold_gain + float(stake.get_dividend_share()) * int(len(historical_data) / 30)
    result_str += str(round(total_buy_hold_gain / float(historical_data[0]['Adj_Close']), 3)) + " total buy and hold return."
    result_str += "\n"
    with open (file, "w") as f:
        f.write (result_str)


#sectortest(startdates = ["2015-01-01", "2015-06-01"],enddates = ["2015-05-01", "2015-10-01"], durations = [20, 50], file = "test2")
# print backtest('AAPL', "2014-01-01", "2015-10-23", 20)
# print backtest('XLK', "2009-01-01", "2015-10-01", 100)
# print ' '.join(sector_info)
# print backtest('XLU', "2003-01-01", "2008-10-01", 200)
# print ' '.join(sector_info)
# realbacktest(ticker = "AAPL", start = "2014-08-01", end = "2015-10-23", duration = 20, commission = 2, file = "test3")
# realbacktest("AAPL", "2014-01-01", "2015-10-23", 20, 2,file="test3")