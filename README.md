# Trading-Bot
This is a coin trading bot working on the 'Upbit' market.
Trades 'DOGE' coins.

- Buys when the current price is [higher than the target price] & [is a bull market - price going over MA5 line]
- Sells at closing price the day coin was bought.

- Backtesting script included. -> Backtesting done to check the estimated profit that can be made given certain target prices.

- Execution command : python main.py
- Environment : python 3.9

- Architecture details : [Coin Trading Strategy.pdf](https://github.com/habinlee/Trading-Bot/files/7066077/Coin.Trading.Strategy.pdf)
