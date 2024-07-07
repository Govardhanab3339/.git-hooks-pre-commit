import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# from api_helper import ShoonyaApiPy
from NorenApi import NorenApi
# import datetime
from datetime import timedelta
from time import sleep
# import pytz
import pyotp
# import pandas as pd
from cls_Symbols_idx_fut import Symbols_Idx_Fut
from cls_Sort_Select_Options import nearestOptions
from cls_Scriptkey_levels import KeyLevels
from cls_Options_ATM_StrikeToSpot_Price import ATMOptionStrike
# from cls_scrpt_quotes import scriptQuotes

import gc

api = NorenApi()

# credentials
user_id    = 'FA108224'
user_pwd     = 'Ram39#Kils'
factor2 = pyotp.TOTP('EETL2QPZ63D25PBN4564T6526R34I77Q').now()  # This should be TOTP
vc      = 'FA108224_U'
app_key = 'df41b1771499934e366634c53f19ac3f'
imei    = 'abc1234'
accesstoken = ''

# api.get_option_chain(exchange='N')

# ret = api.option_greek(expiredate ='26-JUL-2024',StrikePrice='150',SpotPrice  = '200',InitRate  = '100',Volatility = '10',OptionType='CE')

# api.get_daily_price_series

#Trade Options Based on flags set below 0 False , 1 True
def read_flags(file_path):
    flags = {}
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if '=' in line:
                key, value = line.strip().split('=')
                flags[key] = int(value)  # Convert the value to an integer
    return flags

# Path to the flags file
flags_file_path = r'C:\Users\GovardhanLaptop\Downloads\Shoonya_NEW-20240205T090853Z-001\Shoonya_NEW\GovAutoTradingTestCode\Flags.txt'

# print("flags_file_path ", flags_file_path)
def update_flags(symbols_list, condition):
    for symbol in symbols_list:
        if condition(symbol):
            symbol['flag'] = 1
        else:
            symbol['flag'] = 0

# Initialize symbols_list with default flag values
symbols_list = [
    {'exch': 'NSE', 'Symbol': 'Nifty 50', 'Instrument': 'INDEX', 'flag': 0},
    # {'exch': 'NFO', 'Symbol': 'NIFTY', 'Instrument': 'FUTIDX', 'flag': 0},
    {'exch': 'NSE', 'Symbol': 'Nifty Bank', 'Instrument': 'INDEX', 'flag': 0},
    # {'exch': 'NFO', 'Symbol': 'BANKNIFTY', 'Instrument': 'FUTIDX', 'flag': 0},
    # {'exch': 'NSE', 'Symbol': 'Nifty Fin Services', 'Instrument': 'INDEX', 'flag': 0},
    # {'exch': 'NFO', 'Symbol': 'FINNIFTY', 'Instrument': 'FUTIDX', 'flag': 0},
    # {'exch': 'NSE', 'Symbol': 'NIFTY MID SELECT', 'Instrument': 'INDEX', 'flag': 0},
    # {'exch': 'NFO', 'Symbol': 'MIDCPNIFTY', 'Instrument': 'FUTIDX', 'flag': 0},
]

def Sleep_in_Secs_NextRun(file_path):
    # sec = 0
    # print(" sleep file read ...", file_path)
    with open(file_path, 'r') as file:
        sleep = file.read()
        # for line in lines:            
    return sleep

# Path to the flags file
Sleep_in_Secs_NextRun_file_path = r'C:\Users\GovardhanLaptop\Downloads\Shoonya_NEW-20240205T090853Z-001\Shoonya_NEW\GovAutoTradingTestCode\Sleep_In_Secs_Till_NextRun_Chart.txt'

# print("Chart_Sleep_NextRun_file_path ", Sleep_in_Secs_NextRun)

def process_symbols(symbols_list):
    results = []
    for symbol_info in symbols_list:
        if symbol_info['flag'] == 1:
            obj = Symbols_Idx_Fut(exch=symbol_info['exch'], Symbol=symbol_info['Symbol'], Instrument=symbol_info['Instrument'])
            tokens = obj.get_NSE_IDX_NFO_FUT()
            results.append((symbol_info['exch'],symbol_info['Symbol'], symbol_info['Instrument'], tokens))
            del obj
    return results

'''1.need option "symbol" to extract list of CE pe options 
      2.Index or fut tokens to get quotes 
      3. extract to run above based on flag values set at the top above continous while loop to run trade for nifty or banknifty or both 
      4.create and set flag to run trades using futesrs of both nifty and bank nifty or just based on respective indecises 
      5. write code to minimize loss
      6.(Optional)write code to temp kill switch to exit any trades  even killing the temporary till next run '''
      
def Shoonya_login():
    #cpass redentials
    ret=api.login(userid=user_id, password=user_pwd, twoFA=factor2, vendor_code=vc, api_secret=app_key, imei=imei)
    return ret['susertoken']

Shoonya_login()
# loginToken=Shoonya_login()
# print("loginToken ",loginToken)

gc.collect(2)

while True:    
    print(""" **** so save the O,H, L,C  recived from get_Quotes recieved in begining of last trading session 
          to compare aganist todays,this will help analyze morning trend that is about to happen in addition to 
          other data like previous days OHLC and CPR etc \n""") 
    
     # Read and parse the flag values at the beginning of each iteration
    flags = read_flags(flags_file_path)
    print("\n flags ", flags)    
    
    # Define conditions
    conditions = {
        # 'Frm_Lst_Via_Both_Fut_Idx': lambda symbol: True,
        # 'Frm_Lst_Only_via_Idx': lambda symbol: symbol['Instrument'] == 'INDEX',
        # 'Frm_Lst_Only_via_Fut': lambda symbol: symbol['Instrument'] == 'FUTIDX',
        # 'Nifty_Via_Both_Fut_Idx': lambda symbol: symbol['Symbol'] in ['Nifty 50', 'NIFTY'],
        'Nifty_Only_via_Idx': lambda symbol: symbol['Symbol'] in ['Nifty 50', 'NIFTY'] and symbol['Instrument'] == 'INDEX',
        # 'Nifty_Only_via_Fut': lambda symbol: symbol['Symbol'] in ['Nifty 50', 'NIFTY'] and symbol['Instrument'] == 'FUTIDX',
        # 'BankNifty_Via_Both_Fut_Idx': lambda symbol: symbol['Symbol'] in ['Nifty Bank', 'BANKNIFTY'],
        'BankNifty_Only_via_Idx': lambda symbol: symbol['Symbol'] in ['Nifty Bank', 'BANKNIFTY'] and symbol['Instrument'] == 'INDEX',
        # 'BankNifty_Only_via_Fut': lambda symbol: symbol['Symbol'] in ['Nifty Bank', 'BANKNIFTY'] and symbol['Instrument'] == 'FUTIDX',
        # 'FinNifty_Via_Both_Fut_Idx': lambda symbol: symbol['Symbol'] in ['Nifty Fin Services', 'FINNIFTY'],
        # 'FinNifty_Only_via_Idx': lambda symbol: symbol['Symbol'] in ['Nifty Fin Services', 'FINNIFTY'] and symbol['Instrument'] == 'INDEX',
        # 'FinNifty_Only_via_Fut': lambda symbol: symbol['Symbol'] in ['Nifty Fin Services', 'FINNIFTY'] and symbol['Instrument'] == 'FUTIDX',
        # 'MidCpNifty_Via_Both_Fut_Idx': lambda symbol: symbol['Symbol'] in ['NIFTY MID SELECT', 'MIDCPNIFTY'],
        # 'MidCpNifty_Only_via_Idx': lambda symbol: symbol['Symbol'] in ['NIFTY MID SELECT', 'MIDCPNIFTY'] and symbol['Instrument'] == 'INDEX',
        # 'MidCpNifty_Only_via_Fut': lambda symbol: symbol['Symbol'] in ['NIFTY MID SELECT', 'MIDCPNIFTY'] and symbol['Instrument'] == 'FUTIDX'
    }

    # Check and apply each flag condition
    for flag_key, condition in conditions.items():
        if flags.get(flag_key, 0):
            print(f'Executing {flag_key} logic...')
            update_flags(symbols_list, condition)
            break  # Assuming only one condition will be true at a time

    # Print the final symbols_list to verify the changes
    print("\n @130 symbols_list \n", symbols_list)

    # Process symbols and print results
    results = process_symbols(symbols_list)
    print("\n results  ", type(results), ' ', results, "\n")
    
    for exch , symbol, instrument, tokens in results:
        if tokens[0] is not None:
           
            token_var_name = f"{symbol.replace(' ', '_')}_{instrument}_tkn"
            trading_symbol_var_name = f"{symbol.replace(' ', '_')}_{instrument}_TradingSymbol"

            quote_var_name = f"{symbol.replace(' ', '_')}_{instrument}_Quote"
            lp_var_name = f"{symbol.replace(' ', '_')}_{instrument}_indx_lp"
      
            exec(f"{token_var_name} = tokens[0]")
            exec(f"{trading_symbol_var_name} = tokens[1]")

            exec(f"{quote_var_name} = api.get_quotes(exchange=exch, token=str({token_var_name}))")
            exec(f"print('\\n line num 229  get quote {symbol} {instrument} ', {quote_var_name})")

            exec(f"{lp_var_name} = {quote_var_name}['lp']")
            
            # print( f"\n type({quote_var_name}['lp']")
            
            print("symbol " , type(symbol) , " " , symbol)
            
            print("\n instrument " , type(instrument) , " " , instrument)

            obj_opt_Sorted_CE_PE = nearestOptions(Symbol=symbol,Instrument=instrument,)
            opt_SortedByExpiry_ce, opt_SortedByExpiry_pe = obj_opt_Sorted_CE_PE.Sorted_CE_PE_Options()
            
            # print("\n ----->@ line 236 \n opt_SortedByExpiry_ce  type(opt_SortedByExpiry_ce['OptionType'] ) \n ", type(opt_SortedByExpiry_ce['OptionType'].iloc[4] ),"\n opt_SortedByExpiry_ce \n ", opt_SortedByExpiry_pe )
            print("\n ----->@ line 236 \n opt_SortedByExpiry_ce ) \n ", opt_SortedByExpiry_ce ),"\n opt_SortedByExpiry_pe \n ", opt_SortedByExpiry_pe )
            del obj_opt_Sorted_CE_PE

            obj_ATM_Opt_CE_PE = ATMOptionStrike(indx_lp=eval(lp_var_name), ce_opt_SortedByExpiry=opt_SortedByExpiry_ce,
                                                pe_opt_SortedByExpiry=opt_SortedByExpiry_pe)

            (ce_ATM_strike_TradingSymbol, pe_ATM_strike_TradingSymbol, pe_ATM_strike_Token, ce_ATM_strike_Token,
            pe_ATM_strike, ce_ATM_strike) = obj_ATM_Opt_CE_PE.get_ATM_options_strike()

            del opt_SortedByExpiry_ce, opt_SortedByExpiry_pe

            ce_ATM_opt_quote = api.get_quotes('NFO', str(ce_ATM_strike_Token))
            print(f'\n {symbol.replace(' ', '_')} ce_ATM_opt_quote : \n ', ce_ATM_opt_quote)

            pe_ATM_opt_quote = api.get_quotes('NFO', str(pe_ATM_strike_Token))
            print(f'\n {symbol.replace(' ', '_')} pe_ATM_opt_quote : \n ', pe_ATM_opt_quote ,'\n')   

            obj_keyLevels = KeyLevels(f'INDEX_{symbol.replace(" ", "_")}', eval(quote_var_name))
            obj_keyLevels.get_ScriptkeyLevels()
            
            key_levels = [
            'wk52_h', 'wk52_l', 'DaysPrev_close', 'reqst_time', 'ltp', 'DaysHigh', 'DaysLow', 'DaysOpen'
        ]    
            
            for level in key_levels:        
                var_name = f"{instrument}_{symbol.replace(' ', '_')}_{level}"
                exec(f"{var_name} = obj_keyLevels.INDEX_{symbol.replace(' ', '_')}_{level}")
                exec(f"print('{var_name}:', {var_name})")
            
            del obj_keyLevels, quote_var_name

            print(f"\n  {symbol} IDX_DaysPrev_close   ", eval(f"{instrument}_{symbol.replace(' ', '_')}_DaysPrev_close"), 
                ' idx_reqst_time  ', eval(f"{instrument}_{symbol.replace(' ', '_')}_reqst_time"), 
                f"\n {symbol.replace(' ', '_')} idx_wk52_h ", eval(f"{instrument}_{symbol.replace(' ', '_')}_wk52_h"), 
                " idx_wk52_l ", eval(f"{instrument}_{symbol.replace(' ', '_')}_wk52_l"))
            
            time_price_series_var_name = f"{instrument}_{symbol.replace(' ', '_')}_TimePriceSeries"
            exec(f"{time_price_series_var_name} = api.get_time_price_series(exchange=exch, token=str(eval(token_var_name)), interval=5)")
            exec(f"print(f'\\n {instrument}_{symbol.replace(' ', '_')}_TimePriceSeries  ', {time_price_series_var_name})")
            exec(f"del {time_price_series_var_name}")
            
            if instrument=="INDEX":
                exec(f"{trading_symbol_var_name} = symbol")

            daily_price_series_var_name = f"{instrument}_{symbol.replace(' ', '_')}_DailyPriceSeries"
            exec(f"{daily_price_series_var_name} = api.get_daily_price_series(tradingsymbol=str(eval(trading_symbol_var_name)), exchange=exch)")
            print("\n")

            daily_price_series_var_name = f"{instrument}_{symbol.replace(' ', '_')}_DailyPriceSeries"
            exec(f"{daily_price_series_var_name} = api.get_daily_price_series(tradingsymbol=str(eval(trading_symbol_var_name)), exchange=exch)")
            exec(f"print(f'\\n ** Note: Daily price series for indexes will be empty , instead consider daily price series of futures or get quotes of Respective indexes \\n"
                f"daily_price_series({eval(trading_symbol_var_name)}) \\n"
                f"{instrument}_{symbol.replace(' ', '_')}_DailyPriceSeries \\n', {daily_price_series_var_name})")                        
            exec(f"del {daily_price_series_var_name}")            
                        
    gc.collect(2)    
    Sleep_In_Secs=Sleep_in_Secs_NextRun(Sleep_in_Secs_NextRun_file_path)
    print("\n =============================================================================================\n")
    sleep(float(Sleep_In_Secs))