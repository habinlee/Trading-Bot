import pyupbit
import numpy as np
import sys

# OHLCV(open, high, low, close, volume)로 당일 시가, 고가, 저가, 종가, 거래량에 대한 데이터
df = pyupbit.get_ohlcv("KRW-DOGE")

# Get date of each row
def get_date(df):
    rowNames = df.index.values
    return rowNames

# Get target price
def get_target(df, i, k, date_today):

    yesterday = df.iloc[i-1]

    today_open = yesterday["close"]
    yesterday_max = yesterday["high"]
    yesterday_min = yesterday["low"]

    print("Max price of the day before : {}".format(yesterday_max))
    print("Min price of the day before : {}".format(yesterday_min))

    target_price = today_open + (yesterday_max - yesterday_min) * k

    print("The target price of {} is : {}\n".format(date_today, target_price))

    return target_price

# Get Selling Price
def get_sell(df, i):

    tomorrow = df.iloc[i+1]
    today_close = tomorrow["open"]
    
    return today_close

# Get profit 
def get_profit(sell, target):
    return sell - target

# Get ror
def get_ror(sell, target, fee):
    return sell / target - fee

# Get MDD
def get_mdd(cur_max, acc_ror):
    return (cur_max - acc_ror) / cur_max * 100

# Get MA5
def get_ma5(df, i):
    ma5 = df["close"].rolling(window=5).mean()
    return ma5.iloc[i]

# Main function
def get_k(df, i, k, fee, date_today):

    # Target Price
    target_price = get_target(df, i, k, date_today)

    print("The target price of {} is : {}\n".format(date_today, target_price))

    # Selling Price
    sell_price = get_sell(df, i)

    print("The closing price of {} is : {}\n".format(date_today, sell_price))

    # Profit
    profit = get_profit(sell_price, target_price)

    # Max price of today to check if we actually made a purchase this day
    today = df.iloc[i]
    today_max = today["high"]

    # ROR
    ror = get_ror(sell_price, target_price, fee)

    # MA5
    ma5 = get_ma5(df, i)

    # Buy or Not - Result Returned
    if today_max > target_price and today["open"] > ma5:
        print("The coin was bought, {} giving us the profit of {}\n".format(date_today, profit))
        print("The rate of profit today was : {}\n".format(ror))
        return (profit, ror)
    else:
        print("The coin was not bought today")
        print("The rate of profit today was : {}".format(1))
        return (0, 1)

if __name__ == '__main__':
    # Data Frame of wanted duration
    df = df.iloc[-7:-1]
    
    # Charge Fee
    fee = 0.005

    # Variables for storing result values
    max_profit = -sys.maxsize
    max_k = 0
    max_ror = 0
    check_list = {}


    # Loop for checking values for all possible k values
    for k in range(1, 10):
        print("==================================START OF K={}=======================================".format(k))
        
        k = k / 10
        total_profit = 0
        total_ror = 1
        cur_max_ror = -sys.maxsize
        max_mdd = -sys.maxsize

        print("Case k = {}\n".format(k))

        # Looping through eveery day in the duration for each k
        for i  in range(1,len(df) - 1):
            date_today = str(get_date(df)[i])[:10]
            print("--------------------------------START OF DAY : {}--------------------------------".format(date_today))

            # Getting the profit / ROR
            result_by_day = get_k(df, i, k, fee, date_today)
            mp = result_by_day[0]
            ror = result_by_day[1]

            total_profit += mp
            total_ror *= ror

            print("Current ROR for day {} : {}".format(date_today, total_ror))

            # Get MDD
            if (total_ror > cur_max_ror):
                cur_max_ror = total_ror
            
            mdd = get_mdd(cur_max_ror, total_ror)

            if (mdd > max_mdd):
                max_mdd = mdd

            print("Current MDD so far : {}".format(max_mdd))

            print("--------------------------------END OF DAY : {}--------------------------------".format(date_today))

        check_list[k] = (total_profit, total_ror)

        if (total_profit > max_profit):
            max_k = k
            max_profit = total_profit
            max_ror = total_ror


        print("The total of all profits at k = {} is : {}\n".format(k, total_profit))
        print("The total ror at k = {} is : {}\n".format(k, total_ror))
        print("The final MDD for k = {} is : {}".format(k, max_mdd))
        print("==================================END OF K={}=======================================\n".format(k))

    print(str(check_list)+"\n")
    print("The max value of k is {} giving us the profit of {}".format(max_k, max_profit))
    print("The max value of k is {} giving us the profit rate of {}".format(max_k, max_ror))
