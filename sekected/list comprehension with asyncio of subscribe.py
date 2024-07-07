import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import time
import pandas as pd
from datetime import datetime
import pyotp
from NorenApi import NorenApi
import asyncio
from testclassrecieveltp import recieveltp

##############################################
#                   INPUT's                  #
##############################################

# Initialize the API
api = NorenApi()

# Credentials
user_id = 'FA108224'
user_pwd = 'Ram39#Kils'
factor2 = pyotp.TOTP('EETL2QPZ63D25PBN4564T6526R34I77Q').now()  # This should be TOTP
vc = 'FA108224_U'
app_key = 'df41b1771499934e366634c53f19ac3f'
imei = 'abc1234'
accesstoken = ''

def Shoonya_login():
    ret = api.login(userid=user_id, password=user_pwd, twoFA=factor2, vendor_code=vc, api_secret=app_key, imei=imei)
    # print("tokeb ", ret['susertoken'] )
    return ret['susertoken']

async def async_Shoonya_login():
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, Shoonya_login)

# Event handler for feed updates
def event_handler_feed_update(tick_data):
    global LTP, strike_dict
    if 'lp' in tick_data:
        LTP = tick_data['lp']
        sym_tk = tick_data['tk']
        strike_dict.update({sym_tk: LTP})

# Callback when the socket is opened
def open_callback():
    global feed_opened
    feed_opened = True

# Synchronous subscribe function
def subscribe():
    # api.subscribe(['NSE|26000', 'NSE|26009', 'NSE|26037', 'NSE|26074'])
    api.subscribe('NSE|26009')

# Asynchronous subscribe function
async def async_subscribe():
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, subscribe)

# Synchronous websocket start function
def sync_startwebsocket():
    api.start_websocket(
        subscribe_callback=event_handler_feed_update,
        socket_open_callback=open_callback)

# Asynchronous websocket start function
async def async_startwebsocket():
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, sync_startwebsocket)

# Asynchronous function to wait for feed to open
async def wait_for_feed_open():
    global feed_opened
    while not feed_opened:
        await asyncio.sleep(0.01)

NiftLtpObj = recieveltp()
BnknifLtpObj = recieveltp()
MidcpLtpObj = recieveltp()
FinNiftLtpObj = recieveltp()

# Map tokens to their corresponding objects and methods
token_map = {
    '26000': NiftLtpObj.get_optionGreek,
    '26009': BnknifLtpObj.get_optionGreek,
    '26037': MidcpLtpObj.get_optionGreek,
    '26074': FinNiftLtpObj.get_optionGreek
}
      
async def process_ltp(tkn):
    if tkn in strike_dict:
        ltp = strike_dict[tkn]
        tkns = ['26000', '26009', '26037', '26074']
        # ts = [asyncio.create_task(token_map[tkn](ltp=ltp, tkn=tkn)) for t in tkns]
        ts = [asyncio.create_task(token_map[tkn](ltp=ltp)) for tkn in tkns]
        await asyncio.gather(*ts)
    else:
        print(f"{tkn} not found in strike_dict")

async def print_ltp():
    while True:
        print("strike_dict ", strike_dict)
        tkns = ['26000', '26009', '26037', '26074']
        tasks = [asyncio.create_task(process_ltp(t)) for t in tkns]
        await asyncio.gather(*tasks)
        await asyncio.sleep(1)

if __name__ == "__main__":
    strike_dict = {}
    feed_opened = False
    
    asyncio.run(async_Shoonya_login())
    
    # Start the websocket connection asynchronously
    asyncio.run(async_startwebsocket())
    
    # Wait until the feed is opened asynchronously
    asyncio.run(wait_for_feed_open())
    
    # Subscribe asynchronously
    asyncio.run(async_subscribe())
    
    asyncio.run(print_ltp())
