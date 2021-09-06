from logging_system import LoggerFile
from pretty_printer import PPrint
from upbitworker import Upbit
from ai_model import Predictor
import time
import datetime
import sys
import schedule

if __name__ == '__main__':
    # Recieve target trading coin from user
    coin_name = input("Enter the code of the coin you want to trade :").upper()
    coin = "KRW-" + coin_name

    # Printer
    pprinter = PPrint()

    # Logging process
    logger_file = LoggerFile()
    logger = logger_file.logging()

    # logger_file.prevent_reload()

    # Upbit Main function
    upbit = Upbit(coin)

    now = datetime.datetime.now()
    mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)

    print("Start the Upbit trading bot!")
    logger.info("Start the Upbit trading bot!")

    # AI model application
    predictor = Predictor(coin)

    predictor.predict_close_price()
    schedule.every().hour.do(lambda: predictor.predict_close_price())  

    while True:
        try:
            now = datetime.datetime.now()

            k = upbit.get_k()

            ma5 = upbit.get_ma5()

            target_price = upbit.get_target(k)

            schedule.run_pending()

            if mid < now < mid + datetime.delta(seconds=10):

                current_price = upbit.get_ticker({"markets" : coin})[0]['trade_price']

                print("Curent price of the coin is {}".format(current_price))
                logger.info("Curent price of the coin is {}".format(current_price))

                mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)

                query = {
                    'market': coin,
                    'side': 'ask',
                    'volume': str(upbit.get_asset_volume(coin)),
                    'ord_type': 'market',
                } 

                sell_result = upbit.trade_coin(query)
                print('The coin was sold!')
                pprinter.pPrint(sell_result)
                assets = upbit.request_private()
                pprinter.pPrint_multi(assets)

            balance = float(upbit.get_balance())

            print('Your current balance in KRW is : {}'.format(balance))
            logger.info('Your current balance in KRW is : {}'.format(balance))

            if (current_price > target_price) and (current_price > ma5) and (balance * 0.9995 > current_price) and (current_price < predictor.predicted_price):
                
                query = {
                    'market': coin,
                    'side': 'bid',
                    'volume': str((balance * 0.9995) / current_price),
                    'price': str(current_price),
                    'ord_type': 'limit',
                }

                buy_result = upbit.trade_coin(query)
                print('The coin was bought!')
                pprinter.pPrint(buy_result)
                assets = upbit.request_private()
                pprinter.pPrint_multi(assets)

        except:
            print('Error - Terminating Process!')
            logger.info('Error - Terminating Process!')
            sys.exit(1)

        time.sleep(1)