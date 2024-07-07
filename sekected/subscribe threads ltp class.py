import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import time
import pandas as pd
from datetime import datetime
import pyotp
from NorenApi import NorenApi
import threading
from testclassrecieveltp import recieveltp

# # Class definition for recieveltp
# class recieveltp:
#     def __init__(self, ltp, tkn):
#         self.ltp = ltp
#         self.tkn = tkn

#     def PrintRecieved_ltp(self):
#         print("LTP:", self.ltp)
#         print("tkn:", self.tkn)
#         print("exch: NSE")

# Shoonya API setup and login
api = NorenApi()
# api.token_setter()

user_id = 'FA108224'
user_pwd = 'Ram39#Kils'
factor2 = pyotp.TOTP('EETL2QPZ63D25PBN4564T6526R34I77Q').now()
vc = 'FA108224_U'
app_key = 'df41b1771499934e366634c53f19ac3f'
imei = 'abc1234'

def Shoonya_login():
    ret = api.login(userid=user_id, password=user_pwd, twoFA=factor2, vendor_code=vc, api_secret=app_key, imei=imei)
    return ret['susertoken']

Shoonya_login()

# Event handlers
def event_handler_feed_update(tick_data):
    global LTP, strike_dict
    if 'lp' in tick_data:
        LTP = tick_data['lp']
        sym_tk = tick_data['tk']
        strike_dict.update({sym_tk: LTP})

def open_callback():
    global feed_opened
    feed_opened = True

def subscribe():
    api.subscribe(['NSE|26000', 'NSE|26009'])

if __name__ == "__main__":
    strike_dict = {}
    feed_opened = False
    api.start_websocket(
        subscribe_callback=event_handler_feed_update,
        socket_open_callback=open_callback)

    while not feed_opened:
        pass

    threading.Thread(target=subscribe).start()

    while True:
        print("strike_dict", strike_dict)
        for sym_tk in strike_dict:
            ltp = strike_dict[sym_tk]
            nifty50 = recieveltp(ltp=ltp, tkn=sym_tk)
            banknifty = recieveltp(ltp=ltp, tkn=sym_tk)
            threading.Thread(target=nifty50.PrintRecieved_ltp).start()
            threading.Thread(target=banknifty.PrintRecieved_ltp).start()
        time.sleep(1)
