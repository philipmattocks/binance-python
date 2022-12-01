from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
import pandas as pd
import os
from time import sleep


def btc_pairs_trade(msg):
    """ define how to process incoming WebSocket messages """
    if msg['e'] != 'error':
        price['BTCUSDT'] = float(msg['c'])
    else:
        price['error'] = True


api_key = os.environ.get('binance_api')
api_secret = os.environ.get('binance_secret')




# Set the following for test only:
# client.API_URL = 'https://testnet.binance.vision/api'


client = Client(api_key, api_secret)
btc_price = client.get_symbol_ticker(symbol="BTCUSDT")
print(f'current BTCUSDT price is {btc_price}')

price = {'BTCUSDT': None, 'error':False}
# init and start the WebSocket
bsm = ThreadedWebsocketManager()
bsm.start()
bsm.start_symbol_ticker_socket(symbol='BTCUSDT', callback=btc_pairs_trade)

while not price['BTCUSDT']:
    # wait for WebSocket to start streaming data
    sleep(0.1)

while True:
    # error check to make sure WebSocket is working
    if price['error']:
        # stop and restart socket
        bsm.stop()
        sleep(2)
        bsm.start()
        price['error'] = False
    else:
        print(price['BTCUSDT'])
        if price['BTCUSDT'] > 10000:
            try:
                print(f'price is {price["BTCUSDT"]} so ordering!')
                order = client.create_test_order(symbol='BNBBTC',
                                                 quantity=100,
                                                 side=Client.SIDE_BUY,
                                                 type=Client.ORDER_TYPE_MARKET)

                #break
            except Exception as e:
                print(e)

    sleep(1)

bsm.stop()
