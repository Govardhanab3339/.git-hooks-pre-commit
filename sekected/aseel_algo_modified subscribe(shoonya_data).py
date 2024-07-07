#DISCLAIMER:
#1) This sample code is for learning purposes only.
#2) Always be very careful when dealing with codes in which you can place orders in your account.
#3) The actual results may or may not be similar to backtested results. The historical results do not guarantee any profits or losses in the future.
#4) You are responsible for any losses/profits that occur in your account in case you plan to take trades in your account.
#5) Aseem Singhal does not take any responsibility of you running these codes on your account and the corresponding profits and losses that might occur.
#6) The running of the code properly is dependent on a lot of factors such as internet, broker, what changes you have made, etc. So it is always better to keep checking the trades as technology error can come anytime.
#7) This is NOT a tip providing service/code.
#8) This is NOT a software. Its a tool that works as per the inputs given by you.
#9) Slippage is dependent on market conditions.
#10) Option trading and automatic API trading are subject to market risks

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#from api_helper import ShoonyaApiPy
import time
import pandas as pd
from time import sleep
# import xlwings as xw
from datetime import datetime
import pyotp
from NorenApi import  NorenApi
import threading
from testclassrecieveltp import recieveltp
# from NorenApi 

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
    #cpass redentials
    ret=api.login(userid=user_id, password=user_pwd, twoFA=factor2, vendor_code=vc, api_secret=app_key, imei=imei)
    return ret['susertoken']

Shoonya_login()


# sheet = None
# t = 1000
# while t > 0 and sheet is None:
#     try:
#         xw.Book('auto_shoonya.xlsx').set_mock_caller()
#         sheet = xw.Book.caller().sheets['Data']
#     except Exception as str_error:
#         print(t, str_error)
#         t -= 1

def event_handler_feed_update(tick_data):
    global LTP,strike_dict
    # print(datetime.now())
    if 'lp' in tick_data:
        LTP=tick_data['lp']
        # exch = tick_data['e']
        sym_tk = tick_data['tk']
        # sym_ticker = exch + "|" + sym_tk
        # sym_ticker = sym_tk
        strike_dict.update({sym_tk:LTP})
        # for sym_tk, 
    # if 'oi' in tick_data:
    #     OI=tick_data['oi']
    #     exch = tick_data['e']
    #     sym_tk = tick_data['tk']
    #     sym_ticker = exch + "|" + sym_tk
    #     oi_dict.update({sym_ticker:OI})

def open_callback():
    global feed_opened
    feed_opened = True

def subscribe():
    api.subscribe(['NSE|26000', 'NSE|26009' ])

# symb_list=sheet['A2'].expand("down").value
# symbolList = []
# for i in symb_list:
#     if i != None: symbolList.append(i)

# for i in range(len(symbolList)):
#     symbol = symbolList[i]
#     exch = symbol[:3]
#     name = symbol[4:]
#     # sheet[f'v{i+19}'].value = api.searchscrip(exchange=exch, searchtext=name)
#     s = api.searchscrip(exchange=exch, searchtext=name)
#     if s:
#         for k in s['values']:
#             if k['tsym'] == name:
#                 sheet[f'B{i+2}'].value = exch + "|" + k['token']
#                 break

#         if name == "Nifty 50":
#             sheet[f'B{i+2}'].value = exch + "|" + "26000"

#         if name == "Nifty Bank":
#             sheet[f'B{i+2}'].value = exch + "|" + "26009"

#         if name == "Nifty Fin Service":
#             sheet[f'B{i+2}'].value = exch + "|" + "26017"

#     else:
#         token = pd.read_csv(f'https://api.shoonya.com/{exch}_symbols.txt.zip')
#         for j in range(0,len(token)):
#             if(token['TradingSymbol'][j] == name):
#                 sheet[f'B{i+2}'].value = exch + "|" + str(token['Token'][j])

#         if name == "Nifty 50":
#             sheet[f'B{i+2}'].value = exch + "|" + "26000"

#         if name == "Nifty Bank":
#             sheet[f'B{i+2}'].value = exch + "|" + "26009"

#         if name == "Nifty Fin Service":
#             sheet[f'B{i+2}'].value = exch + "|" + "26017"


# inst_list=sheet['B2'].expand("down").value
# instrumentList = []
# for i in inst_list:
#     if i != None: instrumentList.append(i)

if __name__ == "__main__":
    #global api
    # wb = None
    # t = 1000
    # while t > 0 and wb is None:
    #     try:
    #         xw.Book('auto_shoonya.xlsx').set_mock_caller()
    #         wb = xw.Book.caller()
    #         sheet = wb.sheets['Data']
    #     except Exception as str_error:
    #         print(t, str_error)
    #         t -= 1

    strike_dict={}
    # oi_dict={}
    feed_opened = False
    api.start_websocket(
        subscribe_callback=event_handler_feed_update,
        socket_open_callback=open_callback)

    while(feed_opened==False):
        pass

    # subscribe_list = instrumentList

    threading.Thread(target=subscribe).start()
    # nifty50 = threading.Thread(target=recieveltp).start()
    # banknifty=threading.Thread(target=recieveltp).start()

    while True:
        print("strike_dict ", strike_dict)
        for sym_tk  in strike_dict:
            # print("sym_tk ", sym_tk)
            # print("LTP", LTP)
            # nifty50 = threading.Thread(target=recieveltp(ltp=LTP,tkn=sym_tk)).start()
            # banknifty=threading.Thread(target=recieveltp(ltp=LTP,tkn=sym_tk)).start()
            nifty50 = threading.Thread(target=recieveltp(ltp=LTP,tkn=sym_tk))
            banknifty=threading.Thread(target=recieveltp(ltp=LTP,tkn=sym_tk))
            nifty50.PrintRecieved_ltp.start()
            banknifty.PrintRecieved_ltp.start()
        # print("oi_dict ",oi_dict)
        # sheet.range('H2').value=strike_dict
        # sheet.range('J2').value=oi_dict
        # strike_dict
        # oi_dict
        time.sleep(1)
