import sys
import jwt
import uuid
import hashlib
from urllib.parse import urlencode
import requests
import time
import datetime
# from datetime import datetime,timedelta
# from imp import reload
from logging_system import LoggerFile
from best_k import bestK

class Upbit:
    # Initializing the upbit account / API request keys
    def __init__(self, coin):
        self.access_key = 'ZRVwNMcvVWrAGpxp8xkJlTNaHM4yv24VrqpKUV46'
        self.secret_key = 'VgCbEfwStdrm1QwuDwNxgOxDAH5RVcbKRB3PDOvx'
        self.server_url = 'https://api.upbit.com/v1/'
        self.coin = coin

        logger_file = LoggerFile()
        self.logger = logger_file.logging()

    # Request authorization
    def get_auth(self, query=None):

        payload = {'access_key': self.access_key,
                    'nonce': str(uuid.uuid4())}   

        if query is not None:

            query_string = urlencode(query).encode()

            m = hashlib.sha512()
            m.update(query_string)
            query_hash = m.hexdigest()

            payload['query_hash'] = query_hash
            payload['query_hash_alg'] = 'SHA512'           

        jwt_token = jwt.encode(payload, self.secret_key, algorithm="HS256")
        authorize_token = 'Bearer {}'.format(jwt_token)
        headers = {"Authorization": authorize_token}

        return headers

    # Recieving list of personal assets
    def request_private(self):
        headers = self.get_auth()
        res = requests.get(self.server_url + "accounts", headers=headers).json()
        
        print('My assets : {}'.format(res))
        self.logger.info('My assets : {}'.format(res))

        return res

    # Recieving list of available assets on the market
    def request_public(self, query):
        headers = self.get_auth(query)
        res = requests.get(self.server_url + "orders/chance", params=query, headers=headers).json()

        return res

    def get_balance(self):
        private_info = self.request_private()
        balance = private_info[0]['balance']

        return balance

    def get_asset_volume(self, name):
        private_info = self.request_private()
        volume = 0
        for coin in private_info:
            if coin['currency'] == name:
                volume = coin['balance']
        
        return float(volume)

    # Get snapshot of coin at request - today
    def get_ticker(self, query):
        headers = {"Accept" : "application/json"}
        res = requests.request("GET", self.server_url + "ticker", params=query, headers=headers).json()

        self.logger.info("Ticker of the coin is : {}".format(res))

        return res

    # Get candle of coin - minute, day, week, month
    def get_candle(self, query, period):
        headers = {"Accept" : "application/json"}
        res = requests.request("GET", self.server_url + "candles/" + period, headers=headers, params=query).json()

        return res

    def trade_coin(self, query):
        headers = self.get_auth(query)
        res = requests.post(self.server_url + "orders", params=query, headers=headers).json()

        print('The result of the trade is : {}'.format(res))
        self.logger.info('The result of the trade is : {}'.format(res))

        return res

    def get_date(self):
        date = datetime.datetime.now()
        date = date.astimezone(datetime.timezone.utc)
        date = date.strftime("%Y-%m-%d %H:%M:%S")

        return date

    def get_yesterday(self):
        yesterday = self.get_candle({'market' : self.coin, "count" : "2", "to" : self.get_date()}, "days")[1]

        return yesterday


    def get_range(self, k):
        yesterday = self.get_yesterday()

        high_price = yesterday['high_price']
        low_price = yesterday['low_price']

        range = (high_price - low_price) * k

        print('The range is : {}'.format(range))
        self.logger.info('The range is : {}'.format(range))

        return range

    def get_target(self, k):
        today = self.get_ticker({'markets' : self.coin})[0]
        open_price = today['opening_price']

        range = self.get_range(k)

        target_price = open_price + range

        print('Target Price is : {}'.format(target_price))
        self.logger.info('Target Price is : {}'.format(target_price))

        return target_price

    def get_ma5(self):
        days5 = self.get_candle({'market' : self.coin, "count" : "6", "to" : self.get_date()}, "days")[:-1]
        
        close_total = 0
        for day in days5:
            close_total += day['prev_closing_price']

        ma5 = close_total / 5

        print('MA5 is {}'.format(ma5))
        self.logger.info(('MA5 is {}'.format(ma5)))

        return ma5

    def get_ma20(self):
        days20 = self.get_candle({'market' : self.coin, "count" : "21", "to" : self.get_date()}, "days")[:-1]
        
        close_total = 0
        for day in days20:
            close_total += day['prev_closing_price']

        ma20 = close_total / 20

        print('MA20 is {}'.format(ma20))
        self.logger.info(print('MA20 is {}'.format(ma20)))

        return ma20

    def get_k(self):
        print('Getting the record of prices for the past 200 days')
        self.logger.info('Getting the record of prices for the past 200 days')
        # days200 =  self.get_candle({'market' : 'KRW-DOGE', "count" : "200", "to" : self.get_date()}, "days")

        # logger.info(days200)

        # curr_max = -sys.maxsize
        # max_k = 0     

        # for k in range(1, 10):
        #     k = k / 10
        #     print('Calculating for k = {}'.format(k))
        #     logger.info('Calculating for k = {}'.format(k))
        #     total_profit = 0
        #     for i in range(1, len(days200) - 1):
        #         day_target = days200[i]['opening_price'] + (days200[i+1]['high_price'] - days200[i+1]['low_price']) * k
        #         day_sell = days200[i-1]['prev_closing_price']

        #         days5 = self.get_candle({'market' : 'KRW-DOGE', "count" : "6"}, "days")[:-1]
        
        #         close_total = 0
        #         for day in days5:
        #             close_total += day['prev_closing_price']

        #         ma5 = close_total / 5

        #         day_max = days200[i]['high_price']

        #         if  day_max > day_target and days200[i]['opening_price'] > ma5:
        #             total_profit += day_sell - day_target

        #         time.sleep(1)

        #     if total_profit > curr_max:
        #         curr_max = total_profit
        #         max_k = k
            
        #     time.sleep(1)

        k_getter = bestK(self.coin)
        max_vals = k_getter.get_k()
        max_k = max_vals[0]
        max_profit = max_vals[1]


        print('The Maximum k values is {} giving the profit of {}'.format(max_k, max_profit))
        self.logger.info('The Maximum k values is {} giving the profit of {}'.format(max_k, max_profit))

        return max_k