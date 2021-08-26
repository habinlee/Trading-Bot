import pyupbit
import numpy as np
import sys

class bestK:
    def __init__(self):
        self.df = pyupbit.get_ohlcv("KRW-DOGE")
        self.fee = 0.005

    def get_profit(self, k=0.5):
        self.df['range'] = (self.df['high'] - self.df['low']) * k
        self.df['target'] = self.df['open'] + self.df['range'].shift(1)
        self.df['ma5'] = self.df['close'].rolling(window=5).mean().shift(1)
        self.df['bull'] = self.df['open'] > self.df['ma5']

        self.df['profit'] = np.where((self.df['high'] > self.df['target']) & self.df['bull'], self.df['close'] - self.df['target'] - self.fee, 0)

        profit = self.df['profit'].sum()

        return profit

    def get_ror(self, k=0.5):
        self.df['range'] = (self.df['high'] - self.df['low']) * k
        self.df['target'] = self.df['open'] + self.df['range'].shift(1)
        self.df['ma5'] = self.df['close'].rolling(window=5).mean().shift(1)
        self.df['bull'] = self.df['open'] > self.df['ma5']
 
        self.df['ror'] = np.where((self.df['high'] > self.df['target']) & self.df['bull'], self.df['close'] / self.df['target'] - self.fee, 1)
 
        ror = self.df['ror'].cumprod()[-2]

        return ror

    def get_k(self):
        max_ror = -sys.maxsize
        max_k = -sys.maxsize
        max_profit = -sys.maxsize

        for k in np.arange(0.1, 1.0, 0.1):
            ror = self.get_ror(k)
            profit = self.get_profit(k)

            if ror > max_ror:
                max_ror = ror
                max_k = k
                max_profit = profit

        return (max_k, max_profit)            