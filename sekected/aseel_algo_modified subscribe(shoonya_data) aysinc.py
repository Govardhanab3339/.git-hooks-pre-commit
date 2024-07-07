import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import time
import pandas as pd
from datetime import datetime
import pyotp
from NorenApi import NorenApi
import threading
import asyncio

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

##############################################
#                   INPUT's                  #
##############################################
# NSE:ACC   --> NSE|22
# NSE:NTPC  --> NSE|11630

api = NorenApi()
api.token_setter()

# credentials
user_id    = 'FA108224'
user_pwd     = 'Ram39#Kils'
factor2 = pyotp.TOTP('EETL2QPZ63D25PBN4564T6526R34I77Q').now()  # This should be TOTP
vc      = 'FA108224_U'
app_key = 'df41b1771499934e366634c53f19ac3f'
imei    = 'abc1234'
accesstoken = ''

def Shoonya_login():
    ret = api.login(userid=user_id, password=user_pwd, twoFA=factor2, vendor_code=vc, api_secret=app_key, imei=imei)
    return ret['susertoken']

Shoonya_login()

def event_handler_feed_update(tick_data):
    global LTP, strike_dict
    # print(datetime.now())
    if 'lp' in tick_data:
        LTP = tick_data['lp']
        exch = tick_data['e']
        sym_tk = tick_data['tk']
        sym_ticker = exch + "|" + sym_tk
        strike_dict.update({sym_ticker: LTP})

def open_callback():
    global feed_opened
    feed_opened = True

def subscribe():
    api.subscribe(['NSE|26000', 'NSE|26009', 'NSE|26037', 'NSE|26074'])

async def async_subscribe():
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, subscribe)

if __name__ == "__main__":
    strike_dict = {}
    feed_opened = False
    api.start_websocket(
        subscribe_callback=event_handler_feed_update,
        socket_open_callback=open_callback
    )

    while not feed_opened:
        pass

    asyncio.run(async_subscribe())

    while True:
        print("strike_dict ", strike_dict)
        time.sleep(1)
