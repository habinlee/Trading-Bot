import pandas as pd
from fbprophet import Prophet
import pyupbit

class Predictor:
    def __init__(self):
        self.predicted_price = 0
        self.df = pyupbit.get_ohlcv("KRW-DOGE", interval="minute60")

    def predict_close_price(self):
        self.df = self.df.reset_index()
        self.df['ds'] = self.df['index']
        self.df['y'] = self.df['close']
        data = self.df[['ds','y']]
        model = Prophet()
        model.fit(data)
        future = model.make_future_dataframe(periods=24, freq='H')
        forecast = model.predict(future)

        closeDf = forecast[forecast['ds'] == forecast.iloc[-1]['ds'].replace(hour=9)]
        if len(closeDf) == 0:
            closeDf = forecast[forecast['ds'] == data.iloc[-1]['ds'].replace(hour=9)]
        closeValue = closeDf['yhat'].values[0]
        self.predicted_close_price = closeValue
