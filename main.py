from logging_system import LoggerFile
from best_k import bestK
from pretty_printer import PPrint
from upbitworker import Upbit
import time
import datetime
import sys

if __name__ == '__main__':

    # Printer
    pprinter = PPrint()

    # Logging process
    logger_file = LoggerFile()
    logger = logger_file.logging()

    # logger_file.prevent_reload()

    # Upbit Main function
    upbit = Upbit()

    now = datetime.datetime.now()
    mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)

    print("Start the Upbit trading bot!")
    logger.info("Start the Upbit trading bot!")

    while True:
        try:
            now = datetime.datetime.now()

            k = upbit.get_k()

            ma5 = upbit.get_ma5()

            current_price = upbit.get_ticker({"markets" : "KRW-DOGE"})[0]['trade_price']

            print("Curent price of the coin is {}".format(current_price))
            logger.info("Curent price of the coin is {}".format(current_price))

            target_price = upbit.get_target(k)

            if mid < now < mid + datetime.delta(seconds=10):

                mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)

                query = {
                    'market': 'KRW-DOGE',
                    'side': 'ask',
                    'volume': upbit.get_asset_volume('KRW-DOGE'),
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

            if (current_price > target_price) and (current_price > ma5) and balance * 0.995 > current_price:
                query = {
                    'market': 'KRW-DOGE',
                    'side': 'bid',
                    'volume': str((balance * 0.995) / current_price),
                    'price': str(current_price),
                    'ord_type': 'limit',
                }

                buy_result = upbit.trade_coin(query)
                print('The coin was bought!')
                pprinter.pPrint(sell_result)
                assets = upbit.request_private()
                pprinter.pPrint_multi(assets)

        except:
            print('Error - Terminating Process!')
            logger.info('Error - Terminating Process!')
            sys.exit(1)

        time.sleep(1)