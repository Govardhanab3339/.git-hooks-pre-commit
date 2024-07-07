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

import time

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from time import sleep
# import xlwings as xw
import time as tm
from datetime import datetime, timedelta
import pandas_ta as pta    #Pandas TA Libv
import ta
import pandas as pd
from NorenApi import NorenApi
#https://buildmedia.readthedocs.org/media/pdf/technical-analysis-library-in-python/latest/technical-analysis-library-in-python.pdf


# sheet = None
# t = 1000
# while t > 0 and sheet is None:
#     try:
#         xw.Book('auto_shoonya.xlsx').set_mock_caller()
#         cred_sheet = xw.Book.caller().sheets['shoonya_login']
#         sheet = xw.Book.caller().sheets['indicator']
#     except Exception as str_error:
#         print(t, str_error)
#         t -= 1

# app_id = cred_sheet['B2'].value
# access_token = cred_sheet['B4'].value
api = NorenApi()
api.token_setter()

def buy_order(exch,trdsymb,qty,price,trigger,remark):
    global api
    # exch = inst[:3]
    # symb = inst[4:]

    # if(ord_type=="MARKET"):
    #     ord_type="MKT"
    #     price = 0
    # elif(ord_type=="LIMIT"):
    #     ord_type="LMT"

    try:
        order_id = api.place_order(buy_or_sell="B",  #B, S
                                   product_type="I", #C CNC, M NRML, I MIS
                                   exchange=exch,
                                   tradingsymbol=trdsymb,
                                   quantity = qty,
                                   discloseqty=qty,
                                   price_type= 'MKT', #LMT, MKT, SL-LMT, SL-MKT
                                   price = 0,
                                #    trigger_price=trigger,
                                   amo="NO",#YES, NO
                                   retention="DAY",
                                   remarks=remark
                                   )
        print(" => ", trdsymb , order_id['norenordno'] )
        return order_id['norenordno']

    except Exception as e:
        print(" => ", trdsymb , "Failed : {} ".format(e))

def sell_order(exch,trdsymb,qty,ord_type,price,trigger,trading_symbol_type):
    global api
    # exch = inst[:3]
    # symb = inst[4:]

    # if(ord_type=="MARKET"):
    #     ord_type="MKT"
    #     price = 0
    # elif(ord_type=="LIMIT"):
    #     ord_type="LMT"

    try:
        order_id = api.place_order(buy_or_sell="S",  #B, S
                                   product_type="I", #C CNC, M NRML, I MIS
                                   exchange=exch,
                                   tradingsymbol=trdsymb,
                                   quantity = qty,
                                   discloseqty=qty,
                                   price_type= 'MKT', #LMT, MKT, SL-LMT, SL-MKT
                                   price = 0,
                                #    trigger_price=0,
                                   amo="NO",#YES, NO
                                   retention="DAY"
                                   )
        print(" => ", trdsymb , order_id['norenordno'] )
        return order_id['norenordno']

    except Exception as e:
        print(" => ", symb , "Failed : {} ".format(e))


def pop_zeros(items):
    while items[-1] == 0:
        items.pop()

def pop_space(items):
    while items[-1] == None:
        items.pop()

if __name__ == '__main__':

    in_name_list = list()
    in1_param = list()
    in2_param = list()
    in3_param = list()
    in4_param = list()
    in5_param = list()

    #Find 5 indicators and the parameters
    in_name_list=sheet['K4'].expand("down").value
    in1_param=sheet['K4'].expand("right").value
    in2_param=sheet['K5'].expand("right").value
    in3_param=sheet['K6'].expand("right").value
    in4_param=sheet['K7'].expand("right").value
    in5_param=sheet['K8'].expand("right").value

    print(in_name_list)
    print(in1_param)
    print(in2_param)
    print(in3_param)
    print(in4_param)

    try:
        qty=int(sheet['B9'].value)
        ord_type=sheet['B10'].value
        buffer=sheet['F10'].value
        sl_type = sheet['B12'].value
        sl_val = sheet['B13'].value
        tar_type = sheet['B14'].value
        tar_val = sheet['B15'].value
        paper_trading = sheet['B16'].value
        #trail_X = sheet['F12'].value
        #trail_Y = sheet['F13'].value
        symbol_analysis = sheet['H4'].value
        trading_symbol_type = sheet['H11'].value
        trading_symbol_expiry = sheet['H12'].value
        trading_symbol_strike = sheet['H13'].value
        trading_symbol_b_or_s = sheet['H14'].value
        option_symbol_name = sheet['H15'].value
        max_trades = sheet['U16'].value
    except Exception as str_error:
        print("155")

    trigger=0
    prev_row = 38
    current_trade = 0
    first_trade = 0
    number_of_trade = 0
    first_time_run = 1
    current_trade = 0
    current_signal = 0
    first_time_run_close_length = 0
    value1 = 0
    value2 = 0
    value3 = 0
    value4 = 0
    value5 = 0


    while True:
        sheet = None
        t = 1000
        while t > 0 and sheet is None:
            try:
                xw.Book('auto_shoonya.xlsx').set_mock_caller()
                cred_sheet = xw.Book.caller().sheets['shoonya_login']
                sheet = xw.Book.caller().sheets['indicator']
            except Exception as str_error:
                print(t, str_error)
                t -= 1

        try:
            open= sheet['D19'].expand("down").value
            high= sheet['E19'].expand("down").value
            low= sheet['F19'].expand("down").value
            close=sheet['G19'].expand("down").value
            candle_close=sheet['Q19'].expand("down").value

            #pop_zeros(open)
            #pop_zeros(high)
            #pop_zeros(low)
            #pop_zeros(close)
            pop_zeros(candle_close)
            #pop_space(open)
            #pop_space(high)
            #pop_space(low)
            #pop_space(close)
            pop_space(candle_close)

            #current row number as per close
            close_length = len(candle_close)
            if first_time_run == 1:
                first_time_run_close_length = close_length
                first_time_run = 2

            if first_time_run_close_length != close_length:
                first_time_run = 0

            current_row = close_length + 18
            temp_open = open[:close_length]
            temp_high = high[:close_length]
            temp_low = low[:close_length]
            temp_close = close[:close_length]

            #calculate indicator value
            if in1_param[0] == "SMA":
                value1=ta.trend.SMAIndicator(pd.Series(temp_close),int(in1_param[1]),False).sma_indicator().iloc[-1]
            elif in1_param[0] == "SMA_O":
                value1=ta.trend.SMAIndicator(pd.Series(temp_open),int(in1_param[1]),False).sma_indicator().iloc[-1]
            elif in1_param[0] == "SMA_H":
                value1=ta.trend.SMAIndicator(pd.Series(temp_high),int(in1_param[1]),False).sma_indicator().iloc[-1]
            elif in1_param[0] == "SMA_L":
                value1=ta.trend.SMAIndicator(pd.Series(temp_low),int(in1_param[1]),False).sma_indicator().iloc[-1]
            elif in1_param[0] == "EMA":
                value1=ta.trend.EMAIndicator(pd.Series(temp_close),int(in1_param[1]),False).ema_indicator().iloc[-1]
            elif in1_param[0] == "EMA_O":
                value1=ta.trend.EMAIndicator(pd.Series(temp_open),int(in1_param[1]),False).ema_indicator().iloc[-1]
            elif in1_param[0] == "EMA_H":
                value1=ta.trend.EMAIndicator(pd.Series(temp_high),int(in1_param[1]),False).ema_indicator().iloc[-1]
            elif in1_param[0] == "EMA_L":
                value1=ta.trend.EMAIndicator(pd.Series(temp_low),int(in1_param[1]),False).ema_indicator().iloc[-1]
            elif in1_param[0] == "WMA":
                value1=ta.trend.WMAIndicator(pd.Series(temp_close),int(in1_param[1]),False).wma().iloc[-1]
            elif in1_param[0] == "WMA_O":
                value1=ta.trend.WMAIndicator(pd.Series(temp_open),int(in1_param[1]),False).wma().iloc[-1]
            elif in1_param[0] == "WMA_H":
                value1=ta.trend.WMAIndicator(pd.Series(temp_high),int(in1_param[1]),False).wma().iloc[-1]
            elif in1_param[0] == "WMA_L":
                value1=ta.trend.WMAIndicator(pd.Series(temp_low),int(in1_param[1]),False).wma().iloc[-1]
            elif in1_param[0] == "PSAR":
                value1 = ta.trend.PSARIndicator(pd.Series(temp_high), pd.Series(temp_low), pd.Series(temp_close), 0.02, 0.2, False).psar().iloc[-1]
            elif in1_param[0] == "ADX":
                value1 = ta.trend.ADXIndicator(pd.Series(temp_high), pd.Series(temp_low), pd.Series(temp_close), int(in1_param[1]), False).adx().iloc[-1]
            elif in1_param[0] == "RSI":
                value1 = ta.momentum.RSIIndicator(pd.Series(temp_close), int(in1_param[1]), False).rsi().iloc[-1]
            elif in1_param[0] == "ATR":
                value1 = ta.volatility.AverageTrueRange(pd.Series(temp_high), pd.Series(temp_low), pd.Series(temp_close), int(in1_param[1]), False).average_true_range().iloc[-1]
            elif in1_param[0] == "BB HIGH":
                value1 = ta.volatility.BollingerBands(pd.Series(temp_close), int(in1_param[1]), int(in1_param[2]), False).bollinger_hband().iloc[-1]
            elif in1_param[0] == "BB LOW":
                value1 = ta.volatility.BollingerBands(pd.Series(temp_close), int(in1_param[1]), int(in1_param[2]), False).bollinger_lband().iloc[-1]
            elif in1_param[0] == "BB":
                value1 = ta.volatility.BollingerBands(pd.Series(temp_close), int(in1_param[1]), int(in1_param[2]), False).bollinger_mavg().iloc[-1]
            elif in1_param[0] == "SUPERTREND":
                value1=pd.DataFrame(pta.supertrend(pd.Series(temp_high),pd.Series(temp_low),pd.Series(temp_close),int(in1_param[1]),int(in1_param[2]))).iloc[-1][0]
            elif in1_param[0] == "STOCHRSI":
                value1=ta.momentum.StochRSIIndicator(pd.Series(temp_close), int(in1_param[1]), int(in1_param[2]), int(in1_param[3]), False).stochrsi().iloc[-1]
            elif in1_param[0] == "STOCHD":
                value1=ta.momentum.StochRSIIndicator(pd.Series(temp_close), int(in1_param[1]), int(in1_param[2]), int(in1_param[3]), False).stochrsi_d().iloc[-1]
            elif in1_param[0] == "STOCHK":
                value1=ta.momentum.StochRSIIndicator(pd.Series(temp_close), int(in1_param[1]), int(in1_param[2]), int(in1_param[3]), False).stochrsi_k().iloc[-1]
            elif in1_param[0] == "MACD":
                value1=ta.trend.MACD(pd.Series(temp_close), int(in1_param[1]), int(in1_param[2]), int(in1_param[3]), False).macd().iloc[-1]
            elif in1_param[0] == "MACD_HISTOGRAM":
                value1=ta.trend.MACD(pd.Series(temp_close), int(in1_param[1]), int(in1_param[2]), int(in1_param[3]), False).macd_diff().iloc[-1]
            elif in1_param[0] == "MACD_SIGNAL":
                value1=ta.trend.MACD(pd.Series(temp_close), int(in1_param[1]), int(in1_param[2]), int(in1_param[3]), False).macd_signal().iloc[-1]

            if in2_param[0] == "SMA":
                value2=ta.trend.SMAIndicator(pd.Series(temp_close),int(in2_param[1]),False).sma_indicator().iloc[-1]
            elif in2_param[0] == "SMA_O":
                value2=ta.trend.SMAIndicator(pd.Series(temp_open),int(in2_param[1]),False).sma_indicator().iloc[-1]
            elif in2_param[0] == "SMA_H":
                value2=ta.trend.SMAIndicator(pd.Series(temp_high),int(in2_param[1]),False).sma_indicator().iloc[-1]
            elif in2_param[0] == "SMA_L":
                value2=ta.trend.SMAIndicator(pd.Series(temp_low),int(in2_param[1]),False).sma_indicator().iloc[-1]
            elif in2_param[0] == "EMA":
                value2=ta.trend.EMAIndicator(pd.Series(temp_close),int(in2_param[1]),False).ema_indicator().iloc[-1]
            elif in2_param[0] == "EMA_O":
                value2=ta.trend.EMAIndicator(pd.Series(temp_open),int(in2_param[1]),False).ema_indicator().iloc[-1]
            elif in2_param[0] == "EMA_H":
                value2=ta.trend.EMAIndicator(pd.Series(temp_high),int(in2_param[1]),False).ema_indicator().iloc[-1]
            elif in2_param[0] == "EMA_L":
                value2=ta.trend.EMAIndicator(pd.Series(temp_low),int(in2_param[1]),False).ema_indicator().iloc[-1]
            elif in2_param[0] == "WMA":
                value2=ta.trend.WMAIndicator(pd.Series(temp_close),int(in2_param[1]),False).wma().iloc[-1]
            elif in2_param[0] == "WMA_O":
                value2=ta.trend.WMAIndicator(pd.Series(temp_open),int(in2_param[1]),False).wma().iloc[-1]
            elif in2_param[0] == "WMA_H":
                value2=ta.trend.WMAIndicator(pd.Series(temp_high),int(in2_param[1]),False).wma().iloc[-1]
            elif in2_param[0] == "WMA_L":
                value2=ta.trend.WMAIndicator(pd.Series(temp_low),int(in2_param[1]),False).wma().iloc[-1]
            elif in2_param[0] == "PSAR":
                value2 = ta.trend.PSARIndicator(pd.Series(temp_high), pd.Series(temp_low), pd.Series(temp_close), 0.02, 0.2, False).psar().iloc[-1]
            elif in2_param[0] == "ADX":
                value2 = ta.trend.ADXIndicator(pd.Series(temp_high), pd.Series(temp_low), pd.Series(temp_close), int(in2_param[1]), False).adx().iloc[-1]
            elif in2_param[0] == "RSI":
                value2 = ta.momentum.RSIIndicator(pd.Series(temp_close), int(in2_param[1]), False).rsi().iloc[-1]
            elif in2_param[0] == "ATR":
                value2 = ta.volatility.AverageTrueRange(pd.Series(temp_high), pd.Series(temp_low), pd.Series(temp_close), int(in2_param[1]), False).average_true_range().iloc[-1]
            elif in2_param[0] == "BB HIGH":
                value2 = ta.volatility.BollingerBands(pd.Series(temp_close), int(in2_param[1]), int(in2_param[2]), False).bollinger_hband().iloc[-1]
            elif in2_param[0] == "BB LOW":
                value2 = ta.volatility.BollingerBands(pd.Series(temp_close), int(in2_param[1]), int(in2_param[2]), False).bollinger_lband().iloc[-1]
            elif in2_param[0] == "BB":
                value2 = ta.volatility.BollingerBands(pd.Series(temp_close), int(in2_param[1]), int(in2_param[2]), False).bollinger_mavg().iloc[-1]
            elif in2_param[0] == "SUPERTREND":
                value2=pd.DataFrame(pta.supertrend(pd.Series(temp_high),pd.Series(temp_low),pd.Series(temp_close),int(in2_param[1]),int(in2_param[2]))).iloc[-1][0]
            elif in2_param[0] == "STOCHRSI":
                value2=ta.momentum.StochRSIIndicator(pd.Series(temp_close), int(in2_param[1]), int(in2_param[2]), int(in2_param[3]), False).stochrsi().iloc[-1]
            elif in2_param[0] == "STOCHD":
                value2=ta.momentum.StochRSIIndicator(pd.Series(temp_close), int(in2_param[1]), int(in2_param[2]), int(in2_param[3]), False).stochrsi_d().iloc[-1]
            elif in2_param[0] == "STOCHK":
                value2=ta.momentum.StochRSIIndicator(pd.Series(temp_close), int(in2_param[1]), int(in2_param[2]), int(in2_param[3]), False).stochrsi_k().iloc[-1]
            elif in2_param[0] == "MACD":
                value2=ta.trend.MACD(pd.Series(temp_close), int(in2_param[1]), int(in2_param[2]), int(in2_param[3]), False).macd().iloc[-1]
            elif in2_param[0] == "MACD_HISTOGRAM":
                value2=ta.trend.MACD(pd.Series(temp_close), int(in2_param[1]), int(in2_param[2]), int(in2_param[3]), False).macd_diff().iloc[-1]
            elif in2_param[0] == "MACD_SIGNAL":
                value2=ta.trend.MACD(pd.Series(temp_close), int(in2_param[1]), int(in2_param[2]), int(in2_param[3]), False).macd_signal().iloc[-1]


            if in3_param[0] == "SMA":
                value3=ta.trend.SMAIndicator(pd.Series(temp_close),int(in3_param[1]),False).sma_indicator().iloc[-1]
            elif in3_param[0] == "SMA_O":
                value3=ta.trend.SMAIndicator(pd.Series(temp_open),int(in3_param[1]),False).sma_indicator().iloc[-1]
            elif in3_param[0] == "SMA_H":
                value3=ta.trend.SMAIndicator(pd.Series(temp_high),int(in3_param[1]),False).sma_indicator().iloc[-1]
            elif in3_param[0] == "SMA_L":
                value3=ta.trend.SMAIndicator(pd.Series(temp_low),int(in3_param[1]),False).sma_indicator().iloc[-1]
            elif in3_param[0] == "EMA":
                value3=ta.trend.EMAIndicator(pd.Series(temp_close),int(in3_param[1]),False).ema_indicator().iloc[-1]
            elif in3_param[0] == "EMA_O":
                value3=ta.trend.EMAIndicator(pd.Series(temp_open),int(in3_param[1]),False).ema_indicator().iloc[-1]
            elif in3_param[0] == "EMA_H":
                value3=ta.trend.EMAIndicator(pd.Series(temp_high),int(in3_param[1]),False).ema_indicator().iloc[-1]
            elif in3_param[0] == "EMA_L":
                value3=ta.trend.EMAIndicator(pd.Series(temp_low),int(in3_param[1]),False).ema_indicator().iloc[-1]
            elif in3_param[0] == "WMA":
                value3=ta.trend.WMAIndicator(pd.Series(temp_close),int(in3_param[1]),False).wma().iloc[-1]
            elif in3_param[0] == "WMA_O":
                value3=ta.trend.WMAIndicator(pd.Series(temp_open),int(in3_param[1]),False).wma().iloc[-1]
            elif in3_param[0] == "WMA_H":
                value3=ta.trend.WMAIndicator(pd.Series(temp_high),int(in3_param[1]),False).wma().iloc[-1]
            elif in3_param[0] == "WMA_L":
                value3=ta.trend.WMAIndicator(pd.Series(temp_low),int(in3_param[1]),False).wma().iloc[-1]
            elif in3_param[0] == "PSAR":
                value3 = ta.trend.PSARIndicator(pd.Series(temp_high), pd.Series(temp_low), pd.Series(temp_close), 0.02, 0.2, False).psar().iloc[-1]
            elif in3_param[0] == "ADX":
                value3 = ta.trend.ADXIndicator(pd.Series(temp_high), pd.Series(temp_low), pd.Series(temp_close), int(in3_param[1]), False).adx().iloc[-1]
            elif in3_param[0] == "RSI":
                value3 = ta.momentum.RSIIndicator(pd.Series(temp_close), int(in3_param[1]), False).rsi().iloc[-1]
            elif in3_param[0] == "ATR":
                value3 = ta.volatility.AverageTrueRange(pd.Series(temp_high), pd.Series(temp_low), pd.Series(temp_close), int(in3_param[1]), False).average_true_range().iloc[-1]
            elif in3_param[0] == "BB HIGH":
                value3 = ta.volatility.BollingerBands(pd.Series(temp_close), int(in3_param[1]), int(in3_param[2]), False).bollinger_hband().iloc[-1]
            elif in3_param[0] == "BB LOW":
                value3 = ta.volatility.BollingerBands(pd.Series(temp_close), int(in3_param[1]), int(in3_param[2]), False).bollinger_lband().iloc[-1]
            elif in3_param[0] == "BB":
                value3 = ta.volatility.BollingerBands(pd.Series(temp_close), int(in3_param[1]), int(in3_param[2]), False).bollinger_mavg().iloc[-1]
            elif in3_param[0] == "SUPERTREND":
                value3=pd.DataFrame(pta.supertrend(pd.Series(temp_high),pd.Series(temp_low),pd.Series(temp_close),int(in3_param[1]),int(in3_param[2]))).iloc[-1][0]
            elif in3_param[0] == "STOCHRSI":
                value3=ta.momentum.StochRSIIndicator(pd.Series(temp_close), int(in3_param[1]), int(in3_param[2]), int(in3_param[3]), False).stochrsi().iloc[-1]
            elif in3_param[0] == "STOCHD":
                value3=ta.momentum.StochRSIIndicator(pd.Series(temp_close), int(in3_param[1]), int(in3_param[2]), int(in3_param[3]), False).stochrsi_d().iloc[-1]
            elif in3_param[0] == "STOCHK":
                value3=ta.momentum.StochRSIIndicator(pd.Series(temp_close), int(in3_param[1]), int(in3_param[2]), int(in3_param[3]), False).stochrsi_k().iloc[-1]
            elif in3_param[0] == "MACD":
                value3=ta.trend.MACD(pd.Series(temp_close), int(in3_param[1]), int(in3_param[2]), int(in3_param[3]), False).macd().iloc[-1]
            elif in3_param[0] == "MACD_HISTOGRAM":
                value3=ta.trend.MACD(pd.Series(temp_close), int(in3_param[1]), int(in3_param[2]), int(in3_param[3]), False).macd_diff().iloc[-1]
            elif in3_param[0] == "MACD_SIGNAL":
                value3=ta.trend.MACD(pd.Series(temp_close), int(in3_param[1]), int(in3_param[2]), int(in3_param[3]), False).macd_signal().iloc[-1]


            if in4_param[0] == "SMA":
                value4=ta.trend.SMAIndicator(pd.Series(temp_close),int(in4_param[1]),False).sma_indicator().iloc[-1]
            elif in4_param[0] == "SMA_O":
                value4=ta.trend.SMAIndicator(pd.Series(temp_open),int(in4_param[1]),False).sma_indicator().iloc[-1]
            elif in4_param[0] == "SMA_H":
                value4=ta.trend.SMAIndicator(pd.Series(temp_high),int(in4_param[1]),False).sma_indicator().iloc[-1]
            elif in4_param[0] == "SMA_L":
                value4=ta.trend.SMAIndicator(pd.Series(temp_low),int(in4_param[1]),False).sma_indicator().iloc[-1]
            elif in4_param[0] == "EMA":
                value4=ta.trend.EMAIndicator(pd.Series(temp_close),int(in4_param[1]),False).ema_indicator().iloc[-1]
            elif in4_param[0] == "EMA_O":
                value4=ta.trend.EMAIndicator(pd.Series(temp_open),int(in4_param[1]),False).ema_indicator().iloc[-1]
            elif in4_param[0] == "EMA_H":
                value4=ta.trend.EMAIndicator(pd.Series(temp_high),int(in4_param[1]),False).ema_indicator().iloc[-1]
            elif in4_param[0] == "EMA_L":
                value4=ta.trend.EMAIndicator(pd.Series(temp_low),int(in4_param[1]),False).ema_indicator().iloc[-1]
            elif in4_param[0] == "WMA":
                value4=ta.trend.WMAIndicator(pd.Series(temp_close),int(in4_param[1]),False).wma().iloc[-1]
            elif in4_param[0] == "WMA_O":
                value4=ta.trend.WMAIndicator(pd.Series(temp_open),int(in4_param[1]),False).wma().iloc[-1]
            elif in4_param[0] == "WMA_H":
                value4=ta.trend.WMAIndicator(pd.Series(temp_high),int(in4_param[1]),False).wma().iloc[-1]
            elif in4_param[0] == "WMA_L":
                value4=ta.trend.WMAIndicator(pd.Series(temp_low),int(in4_param[1]),False).wma().iloc[-1]
            elif in4_param[0] == "PSAR":
                value4 = ta.trend.PSARIndicator(pd.Series(temp_high), pd.Series(temp_low), pd.Series(temp_close), 0.02, 0.2, False).psar().iloc[-1]
            elif in4_param[0] == "ADX":
                value4 = ta.trend.ADXIndicator(pd.Series(temp_high), pd.Series(temp_low), pd.Series(temp_close), int(in4_param[1]), False).adx().iloc[-1]
            elif in4_param[0] == "RSI":
                value4 = ta.momentum.RSIIndicator(pd.Series(temp_close), int(in4_param[1]), False).rsi().iloc[-1]
            elif in4_param[0] == "ATR":
                value4 = ta.volatility.AverageTrueRange(pd.Series(temp_high), pd.Series(temp_low), pd.Series(temp_close), int(in4_param[1]), False).average_true_range().iloc[-1]
            elif in4_param[0] == "BB HIGH":
                value4 = ta.volatility.BollingerBands(pd.Series(temp_close), int(in4_param[1]), int(in4_param[2]), False).bollinger_hband().iloc[-1]
            elif in4_param[0] == "BB LOW":
                value4 = ta.volatility.BollingerBands(pd.Series(temp_close), int(in4_param[1]), int(in4_param[2]), False).bollinger_lband().iloc[-1]
            elif in4_param[0] == "BB":
                value4 = ta.volatility.BollingerBands(pd.Series(temp_close), int(in4_param[1]), int(in4_param[2]), False).bollinger_mavg().iloc[-1]
            elif in4_param[0] == "SUPERTREND":
                value4=pd.DataFrame(pta.supertrend(pd.Series(temp_high),pd.Series(temp_low),pd.Series(temp_close),int(in4_param[1]),int(in4_param[2]))).iloc[-1][0]
            elif in4_param[0] == "STOCHRSI":
                value4=ta.momentum.StochRSIIndicator(pd.Series(temp_close), int(in4_param[1]), int(in4_param[2]), int(in4_param[3]), False).stochrsi().iloc[-1]
            elif in4_param[0] == "STOCHD":
                value4=ta.momentum.StochRSIIndicator(pd.Series(temp_close), int(in4_param[1]), int(in4_param[2]), int(in4_param[3]), False).stochrsi_d().iloc[-1]
            elif in4_param[0] == "STOCHK":
                value4=ta.momentum.StochRSIIndicator(pd.Series(temp_close), int(in4_param[1]), int(in4_param[2]), int(in4_param[3]), False).stochrsi_k().iloc[-1]
            elif in4_param[0] == "MACD":
                value4=ta.trend.MACD(pd.Series(temp_close), int(in4_param[1]), int(in4_param[2]), int(in4_param[3]), False).macd().iloc[-1]
            elif in4_param[0] == "MACD_HISTOGRAM":
                value4=ta.trend.MACD(pd.Series(temp_close), int(in4_param[1]), int(in4_param[2]), int(in4_param[3]), False).macd_diff().iloc[-1]
            elif in4_param[0] == "MACD_SIGNAL":
                value4=ta.trend.MACD(pd.Series(temp_close), int(in4_param[1]), int(in4_param[2]), int(in4_param[3]), False).macd_signal().iloc[-1]


            if in5_param[0] == "SMA":
                value5=ta.trend.SMAIndicator(pd.Series(temp_close),int(in5_param[1]),False).sma_indicator().iloc[-1]
            elif in5_param[0] == "SMA_O":
                value5=ta.trend.SMAIndicator(pd.Series(temp_open),int(in5_param[1]),False).sma_indicator().iloc[-1]
            elif in5_param[0] == "SMA_H":
                value5=ta.trend.SMAIndicator(pd.Series(temp_high),int(in5_param[1]),False).sma_indicator().iloc[-1]
            elif in5_param[0] == "SMA_L":
                value5=ta.trend.SMAIndicator(pd.Series(temp_low),int(in5_param[1]),False).sma_indicator().iloc[-1]
            elif in5_param[0] == "EMA":
                value5=ta.trend.EMAIndicator(pd.Series(temp_close),int(in5_param[1]),False).ema_indicator().iloc[-1]
            elif in5_param[0] == "EMA_O":
                value5=ta.trend.EMAIndicator(pd.Series(temp_open),int(in5_param[1]),False).ema_indicator().iloc[-1]
            elif in5_param[0] == "EMA_H":
                value5=ta.trend.EMAIndicator(pd.Series(temp_high),int(in5_param[1]),False).ema_indicator().iloc[-1]
            elif in5_param[0] == "EMA_L":
                value5=ta.trend.EMAIndicator(pd.Series(temp_low),int(in5_param[1]),False).ema_indicator().iloc[-1]
            elif in5_param[0] == "WMA":
                value5=ta.trend.WMAIndicator(pd.Series(temp_close),int(in5_param[1]),False).wma().iloc[-1]
            elif in5_param[0] == "WMA_O":
                value5=ta.trend.WMAIndicator(pd.Series(temp_open),int(in5_param[1]),False).wma().iloc[-1]
            elif in5_param[0] == "WMA_H":
                value5=ta.trend.WMAIndicator(pd.Series(temp_high),int(in5_param[1]),False).wma().iloc[-1]
            elif in5_param[0] == "WMA_L":
                value5=ta.trend.WMAIndicator(pd.Series(temp_low),int(in5_param[1]),False).wma().iloc[-1]
            elif in5_param[0] == "PSAR":
                value5 = ta.trend.PSARIndicator(pd.Series(temp_high), pd.Series(temp_low), pd.Series(temp_close), 0.02, 0.2, False).psar().iloc[-1]
            elif in5_param[0] == "ADX":
                value5 = ta.trend.ADXIndicator(pd.Series(temp_high), pd.Series(temp_low), pd.Series(temp_close), int(in5_param[1]), False).adx().iloc[-1]
            elif in5_param[0] == "RSI":
                value5 = ta.momentum.RSIIndicator(pd.Series(temp_close), int(in5_param[1]), False).rsi().iloc[-1]
            elif in5_param[0] == "ATR":
                value5 = ta.volatility.AverageTrueRange(pd.Series(temp_high), pd.Series(temp_low), pd.Series(temp_close), int(in5_param[1]), False).average_true_range().iloc[-1]
            elif in5_param[0] == "BB HIGH":
                value5 = ta.volatility.BollingerBands(pd.Series(temp_close), int(in5_param[1]), int(in5_param[2]), False).bollinger_hband().iloc[-1]
            elif in5_param[0] == "BB LOW":
                value5 = ta.volatility.BollingerBands(pd.Series(temp_close), int(in5_param[1]), int(in5_param[2]), False).bollinger_lband().iloc[-1]
            elif in5_param[0] == "BB":
                value5 = ta.volatility.BollingerBands(pd.Series(temp_close), int(in5_param[1]), int(in5_param[2]), False).bollinger_mavg().iloc[-1]
            elif in5_param[0] == "SUPERTREND":
                value5=pd.DataFrame(pta.supertrend(pd.Series(temp_high),pd.Series(temp_low),pd.Series(temp_close),int(in5_param[1]),int(in5_param[2]))).iloc[-1][0]
            elif in5_param[0] == "STOCHRSI":
                value5=ta.momentum.StochRSIIndicator(pd.Series(temp_close), int(in5_param[1]), int(in5_param[2]), int(in5_param[3]), False).stochrsi().iloc[-1]
            elif in5_param[0] == "STOCHD":
                value5=ta.momentum.StochRSIIndicator(pd.Series(temp_close), int(in5_param[1]), int(in5_param[2]), int(in5_param[3]), False).stochrsi_d().iloc[-1]
            elif in5_param[0] == "STOCHK":
                value5=ta.momentum.StochRSIIndicator(pd.Series(temp_close), int(in5_param[1]), int(in5_param[2]), int(in5_param[3]), False).stochrsi_k().iloc[-1]
            elif in5_param[0] == "MACD":
                value5=ta.trend.MACD(pd.Series(temp_close), int(in5_param[1]), int(in5_param[2]), int(in5_param[3]), False).macd().iloc[-1]
            elif in5_param[0] == "MACD_HISTOGRAM":
                value5=ta.trend.MACD(pd.Series(temp_close), int(in5_param[1]), int(in5_param[2]), int(in5_param[3]), False).macd_diff().iloc[-1]
            elif in5_param[0] == "MACD_SIGNAL":
                value5=ta.trend.MACD(pd.Series(temp_close), int(in5_param[1]), int(in5_param[2]), int(in5_param[3]), False).macd_signal().iloc[-1]

        except Exception as str_error:
            print("488")

        try:
            #Update value of indicator in excel
            sheet[f'I{current_row}'].value = value1
            sheet[f'J{current_row}'].value = value2
            sheet[f'K{current_row}'].value = value3
            sheet[f'L{current_row}'].value = value4
            sheet[f'M{current_row}'].value = value5

            #check current signal
            current_signal = sheet[f'U{current_row}'].value
            close_price = sheet[f'G{current_row}'].value
            next_row_high_price = sheet[f'E{current_row + 1}'].value
            next_row_low_price = sheet[f'F{current_row + 1}'].value


        except Exception as str_error:
            print("506")

        #take trade if firsttrade
        if current_trade == 0 and (current_signal == "BUY" or current_signal == "SELL") and first_time_run == 0 and number_of_trade < max_trades:
            current_trade = current_signal
            number_of_trade = number_of_trade + 1
            entry_price = close_price

            if current_trade == "BUY":
                status = "BUY ENTRY"
                #calculate sl_price and target_price
                if sl_type == "Point":
                    sl_price = entry_price - sl_val
                else:
                    sl_price = entry_price * (1-sl_val/100)

                if tar_type == "Point":
                    tar_price = entry_price + tar_val
                else:
                    tar_price = entry_price * (1 + tar_val/100)


                price = entry_price + buffer
                if trading_symbol_type == "OPTION":
                    #Create trading symbol
                    strike_to_trade = round(entry_price/trading_symbol_strike,0)*trading_symbol_strike
                    if trading_symbol_b_or_s == "BUYER":
                        symbol_trading = "NFO:" + option_symbol_name + str(trading_symbol_expiry) + "C" + str(strike_to_trade)
                        if paper_trading == 1:
                            ord_id=1
                        else:
                            ord_id=buy_order(symbol_trading, qty, ord_type, float(price), float(trigger))
                    else:
                        symbol_trading = "NFO:" + option_symbol_name + str(trading_symbol_expiry) + "P" + str(strike_to_trade)
                        if paper_trading == 1:
                            ord_id=1
                        else:
                            ord_id=sell_order(symbol_trading, qty, ord_type, float(price), float(trigger))

                else:
                    symbol_trading = symbol_analysis
                    if paper_trading == 1:
                        ord_id=1
                    else:
                        ord_id=buy_order(symbol_analysis, qty, ord_type, float(price), float(trigger))

            elif current_trade == "SELL":
                status = "SELL ENTRY"
                #calculate sl_price and target_price
                if sl_type == "Point":
                    sl_price = entry_price + sl_val
                else:
                    sl_price = entry_price * (1+sl_val/100)

                if tar_type == "Point":
                    tar_price = entry_price - tar_val
                else:
                    tar_price = entry_price * (1 - tar_val/100)


                price = entry_price - buffer
                if trading_symbol_type == "OPTION":
                    #Create trading symbol
                    strike_to_trade = round(entry_price/trading_symbol_strike,0)*trading_symbol_strike
                    if trading_symbol_b_or_s == "BUYER":
                        symbol_trading = "NFO:" + option_symbol_name + str(trading_symbol_expiry) + "P" + str(strike_to_trade)
                        if paper_trading == 1:
                            ord_id=1
                        else:
                            ord_id=buy_order(symbol_trading, qty, ord_type, float(price), float(trigger))
                    else:
                        symbol_trading = "NFO:" + option_symbol_name + str(trading_symbol_expiry) + "C" + str(strike_to_trade)
                        if paper_trading == 1:
                            ord_id=1
                        else:
                            ord_id=sell_order(symbol_trading, qty, ord_type, float(price), float(trigger))

                else:
                    symbol_trading = symbol_analysis
                    if paper_trading == 1:
                        ord_id=1
                    else:
                        ord_id=sell_order(symbol_analysis, qty, ord_type, float(price), float(trigger))

            #Update values in Excel
            try:
                sheet[f'W{current_row}'].value = entry_price
                sheet[f'X{current_row}'].value = sl_price
                sheet[f'Y{current_row}'].value = tar_price
                sheet[f'Z{current_row}'].value = status
                sheet[f'AA{current_row}'].value = ord_id
                sheet[f'AD{current_row}'].value = symbol_trading
            except Exception as str_error:
                print("599")


        #check if Stop loss or target hit
        if current_trade == "BUY" and next_row_high_price >= tar_price:
            status = "BUY TARGET"
            current_trade = 1
            exit_price = tar_price
            if paper_trading == 1:
                ord_id=1
            else:
                if trading_symbol_type == "OPTION":
                    if trading_symbol_b_or_s == "BUYER":
                        ord_id=sell_order(symbol_trading, qty, "MARKET", 0, 0)
                    else:
                        ord_id=buy_order(symbol_trading, qty, "MARKET", 0, 0)
                else:
                    ord_id=sell_order(symbol_trading, qty, "MARKET", 0, 0)

            try:
                sheet[f'Z{current_row}'].value = status
                sheet[f'AB{current_row}'].value = exit_price
                sheet[f'AC{current_row}'].value = ord_id
                sheet[f'AD{current_row}'].value = symbol_trading
            except Exception as str_error:
                print("624")

        elif current_trade == "BUY" and next_row_low_price <= sl_price:
            status = "BUY SL"
            current_trade = 0
            exit_price = sl_price
            if paper_trading == 1:
                ord_id=1
            else:
                if trading_symbol_type == "OPTION":
                    if trading_symbol_b_or_s == "BUYER":
                        ord_id=sell_order(symbol_trading, qty, "MARKET", 0, 0)
                    else:
                        ord_id=buy_order(symbol_trading, qty, "MARKET", 0, 0)
                else:
                    ord_id=sell_order(symbol_trading, qty, "MARKET", 0, 0)

            try:
                sheet[f'Z{current_row}'].value = status
                sheet[f'AB{current_row}'].value = exit_price
                sheet[f'AC{current_row}'].value = ord_id
                sheet[f'AD{current_row}'].value = symbol_trading
            except Exception as str_error:
                print("647")

        elif current_trade == "SELL" and next_row_low_price <= tar_price:
            status = "SELL TARGET"
            current_trade = 1
            exit_price = tar_price
            if paper_trading == 1:
                ord_id=1
            else:
                if trading_symbol_type == "OPTION":
                    if trading_symbol_b_or_s == "BUYER":
                        ord_id=sell_order(symbol_trading, qty, "MARKET", 0, 0)
                    else:
                        ord_id=buy_order(symbol_trading, qty, "MARKET", 0, 0)
                else:
                    ord_id=buy_order(symbol_trading, qty, "MARKET", 0, 0)

            try:
                sheet[f'Z{current_row}'].value = status
                sheet[f'AB{current_row}'].value = exit_price
                sheet[f'AC{current_row}'].value = ord_id
                sheet[f'AD{current_row}'].value = symbol_trading
            except Exception as str_error:
                print("670")

        elif current_trade == "SELL" and next_row_high_price >= sl_price:
            status = "SELL SL"
            current_trade = 0
            exit_price = sl_price
            if paper_trading == 1:
                ord_id=1
            else:
                if trading_symbol_type == "OPTION":
                    if trading_symbol_b_or_s == "BUYER":
                        ord_id=sell_order(symbol_trading, qty, "MARKET", 0, 0)
                    else:
                        ord_id=buy_order(symbol_trading, qty, "MARKET", 0, 0)
                else:
                    ord_id=buy_order(symbol_trading, qty, "MARKET", 0, 0)

            try:
                sheet[f'Z{current_row}'].value = status
                sheet[f'AB{current_row}'].value = exit_price
                sheet[f'AC{current_row}'].value = ord_id
                sheet[f'AD{current_row}'].value = symbol_trading
            except Exception as str_error:
                print("693")


        #check for reversal trade
        if current_trade == "BUY" and current_signal == "SELL":
            status = "REVERSAL SELL"
            current_trade = "SELL"
            exit_price = close_price
            if paper_trading == 1:
                ord_id_exit=1
            else:
                if trading_symbol_type == "OPTION":
                    if trading_symbol_b_or_s == "BUYER":
                        ord_id_exit=sell_order(symbol_trading, qty, "MARKET", 0, 0)
                    else:
                        ord_id_exit=buy_order(symbol_trading, qty, "MARKET", 0, 0)
                else:
                    ord_id_exit=sell_order(symbol_trading, qty, "MARKET", 0, 0)

            try:
                sheet[f'Z{current_row}'].value = status
                sheet[f'AB{current_row}'].value = exit_price
                sheet[f'AC{current_row}'].value = ord_id_exit
                sheet[f'AD{current_row}'].value = symbol_trading
            except Exception as str_error:
                print("718")

            if (number_of_trade < max_trades):
                number_of_trade = number_of_trade + 1
                entry_price = close_price

                #calculate sl_price and target_price
                if sl_type == "Point":
                    sl_price = entry_price + sl_val
                else:
                    sl_price = entry_price * (1+sl_val/100)

                if tar_type == "Point":
                    tar_price = entry_price - tar_val
                else:
                    tar_price = entry_price * (1 - tar_val/100)


                price = entry_price - buffer
                if trading_symbol_type == "OPTION":
                    #Create trading symbol
                    strike_to_trade = round(entry_price/trading_symbol_strike,0)*trading_symbol_strike
                    if trading_symbol_b_or_s == "BUYER":
                        symbol_trading = "NFO:" + option_symbol_name + str(trading_symbol_expiry) + "P" + str(strike_to_trade)
                        if paper_trading == 1:
                            ord_id=1
                        else:
                            ord_id=buy_order(symbol_trading, qty, ord_type, float(price), float(trigger))
                    else:
                        symbol_trading = "NFO:" + option_symbol_name + str(trading_symbol_expiry) + "C" + str(strike_to_trade)
                        if paper_trading == 1:
                            ord_id=1
                        else:
                            ord_id=sell_order(symbol_trading, qty, ord_type, float(price), float(trigger))

                else:
                    symbol_trading = symbol_analysis
                    if paper_trading == 1:
                        ord_id=1
                    else:
                        ord_id=sell_order(symbol_analysis, qty, ord_type, float(price), float(trigger))

                try:
                    sheet[f'W{current_row}'].value = entry_price
                    sheet[f'X{current_row}'].value = sl_price
                    sheet[f'Y{current_row}'].value = tar_price
                    sheet[f'Z{current_row}'].value = status
                    sheet[f'AA{current_row}'].value = ord_id
                    sheet[f'AB{current_row}'].value = exit_price
                    sheet[f'AC{current_row}'].value = ord_id_exit
                    sheet[f'AD{current_row}'].value = symbol_trading
                except Exception as str_error:
                    print("770")

        elif current_trade == "SELL" and current_signal == "BUY":
            status = "REVERSAL BUY"
            current_trade = "BUY"
            exit_price = close_price
            if paper_trading == 1:
                ord_id_exit=1
            else:
                if trading_symbol_type == "OPTION":
                    if trading_symbol_b_or_s == "BUYER":
                        ord_id_exit=sell_order(symbol_trading, qty, "MARKET", 0, 0)
                    else:
                        ord_id_exit=buy_order(symbol_trading, qty, "MARKET", 0, 0)
                else:
                    ord_id_exit=buy_order(symbol_trading, qty, "MARKET", 0, 0)

            try:
                sheet[f'Z{current_row}'].value = status
                sheet[f'AB{current_row}'].value = exit_price
                sheet[f'AC{current_row}'].value = ord_id_exit
                sheet[f'AD{current_row}'].value = symbol_trading
            except Exception as str_error:
                print("793")

            if (number_of_trade < max_trades):
                number_of_trade = number_of_trade + 1
                entry_price = close_price

                #calculate sl_price and target_price
                if sl_type == "Point":
                    sl_price = entry_price - sl_val
                else:
                    sl_price = entry_price * (1-sl_val/100)

                if tar_type == "Point":
                    tar_price = entry_price + tar_val
                else:
                    tar_price = entry_price * (1 + tar_val/100)


                price = entry_price + buffer
                if trading_symbol_type == "OPTION":
                    #Create trading symbol
                    strike_to_trade = round(entry_price/trading_symbol_strike,0)*trading_symbol_strike
                    if trading_symbol_b_or_s == "BUYER":
                        symbol_trading = "NFO:" + option_symbol_name + str(trading_symbol_expiry) + "C" + str(strike_to_trade)
                        if paper_trading == 1:
                            ord_id=1
                        else:
                            ord_id=buy_order(symbol_trading, qty, ord_type, float(price), float(trigger))
                    else:
                        symbol_trading = "NFO:" + option_symbol_name + str(trading_symbol_expiry) + "P" + str(strike_to_trade)
                        if paper_trading == 1:
                            ord_id=1
                        else:
                            ord_id=sell_order(symbol_trading, qty, ord_type, float(price), float(trigger))

                else:
                    symbol_trading = symbol_analysis
                    if paper_trading == 1:
                        ord_id=1
                    else:
                        ord_id=buy_order(symbol_analysis, qty, ord_type, float(price), float(trigger))

                try:
                    sheet[f'W{current_row}'].value = entry_price
                    sheet[f'X{current_row}'].value = sl_price
                    sheet[f'Y{current_row}'].value = tar_price
                    sheet[f'Z{current_row}'].value = status
                    sheet[f'AA{current_row}'].value = ord_id
                    sheet[f'AB{current_row}'].value = exit_price
                    sheet[f'AC{current_row}'].value = ord_id_exit
                    sheet[f'AD{current_row}'].value = symbol_trading
                except Exception as str_error:
                    print("845")

        #Check for time exit
        time_exit = sheet['C7'].value
        if time_exit == 1 and current_trade == "BUY":
            status = "BUY TIME EXIT"
            current_trade = 1
            exit_price = close_price
            if paper_trading == 1:
                ord_id=1
            else:
                if trading_symbol_type == "OPTION":
                    if trading_symbol_b_or_s == "BUYER":
                        ord_id=sell_order(symbol_trading, qty, "MARKET", 0, 0)
                    else:
                        ord_id=buy_order(symbol_trading, qty, "MARKET", 0, 0)
                else:
                    ord_id=sell_order(symbol_trading, qty, "MARKET", 0, 0)

            try:
                sheet[f'Z{current_row}'].value = status
                sheet[f'AB{current_row}'].value = exit_price
                sheet[f'AC{current_row}'].value = ord_id
                sheet[f'AD{current_row}'].value = symbol_trading
            except Exception as str_error:
                print("870")
        elif time_exit == 1 and current_trade == "SELL":
            status = "SELL TIME EXIT"
            current_trade = 1
            exit_price = close_price
            if paper_trading == 1:
                ord_id=1
            else:
                if trading_symbol_type == "OPTION":
                    if trading_symbol_b_or_s == "BUYER":
                        ord_id=sell_order(symbol_trading, qty, "MARKET", 0, 0)
                    else:
                        ord_id=buy_order(symbol_trading, qty, "MARKET", 0, 0)
                else:
                    ord_id=buy_order(symbol_trading, qty, "MARKET", 0, 0)

            try:
                sheet[f'Z{current_row}'].value = status
                sheet[f'AB{current_row}'].value = exit_price
                sheet[f'AC{current_row}'].value = ord_id
                sheet[f'AD{current_row}'].value = symbol_trading
            except Exception as str_error:
                print("892")

        time.sleep(5)
        print(datetime.now())