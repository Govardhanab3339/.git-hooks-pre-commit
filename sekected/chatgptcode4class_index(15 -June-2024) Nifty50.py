import os
import sys
import datetime
from datetime import timedelta
from time import sleep
# import json
import pytz
import pyotp
import pandas as pd
import numpy as np
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from NorenApi import NorenApi

#start of our program
api = NorenApi()

# credentials
user_id    = 'FA108224'
user_pwd     = 'Ram39#Kils'
# api = NorenApi()
factor2 = pyotp.TOTP('EETL2QPZ63D25PBN4564T6526R34I77Q').now()  # This should be TOTP
vc      = 'FA108224_U'
app_key = 'df41b1771499934e366634c53f19ac3f'
imei    = 'abc1234'
accesstoken = ''

def Shoonya_login():
    #cpass redentials
    ret=api.login(userid=user_id, password=user_pwd, twoFA=factor2, vendor_code=vc, api_secret=app_key, imei=imei)
    return ret['susertoken']

# print("login ", Shoonya_login())

login_token=Shoonya_login()
# print("\n login_token  ", login_token)

'''print("""check if we can get the options historicaldata usng the get price 
          series method and write code to fetch CE and PE for respective optons to know te price
           moment and also use the greeks values to evaluate on which option to enter and which option to exit""")'''
idx_NSE_NIFTY50_tkn='26000'
idx_NSE_NIFTY50_Symbol='Nifty 50'
idx_NSE_NIFTY50_TradingSymbol='NIFTY INDEX'

    
def get_NFO_OPT():      
    # print("""**** code to  consume NSE , and symbol  "Nifty 50 or Nifty Bank" and return output values for related to 
    #         respective index , "current weeks " futures and options having exchange and tokens  for each which are needed 
    #         to be passesd for web socket subscribe() method  like [{ "EXCH :NSE" , token : 2900, IntType: Index } , 
    #         { "EXCH :NFO" , token : 4892, IntType: FUTidx} , { "EXCH :NFO" , token : 7895, IntType: OPTIDX} \n """)        
           
    NFO_symbol_df = pd.read_csv(f'https://api.shoonya.com/{"NFO"}_symbols.txt.zip')
            
    NFO_NIFTY_FUT_boolean_mask = ( NFO_symbol_df['Symbol'].isin(['NIFTY']) ) & (NFO_symbol_df['Instrument'].isin(['FUTIDX']))
    filtered_NFO_NIFTY_FUT_df = NFO_symbol_df[NFO_NIFTY_FUT_boolean_mask]
    # print("*** filtered_NFO_NIFTY_FUT_df @ line 111 \n", filtered_NFO_NIFTY_FUT_df)
    
    filtered_NFO_NIFTY_FUT_df.loc[filtered_NFO_NIFTY_FUT_df.index, 'Expiry'] = pd.to_datetime(filtered_NFO_NIFTY_FUT_df['Expiry'], format='%d-%b-%Y')
    Sorted_filtered_NFO_NIFTY_FUT_df = filtered_NFO_NIFTY_FUT_df.sort_values(by='Expiry')
    # print("line 115 : sorted NIFTY futidx \n", Sorted_filtered_NFO_NIFTY_FUT_df)
    
    NFO_BANKNIFTY_FUT_boolean_mask = ( NFO_symbol_df['Symbol'].isin(['BANKNIFTY']) ) & (NFO_symbol_df['Instrument'].isin(['FUTIDX']))
    filtered_NFO_BANKNIFTY_FUT_df = NFO_symbol_df[NFO_BANKNIFTY_FUT_boolean_mask]
    # print("*** filtered_NFO_BANKNIFTY_FUT_df @ line 119 \n", filtered_NFO_BANKNIFTY_FUT_df)
    
    filtered_NFO_BANKNIFTY_FUT_df.loc[filtered_NFO_BANKNIFTY_FUT_df.index, 'Expiry'] = pd.to_datetime(filtered_NFO_BANKNIFTY_FUT_df['Expiry'], format='%d-%b-%Y')
    Sorted_filtered_NFO_BANKNIFTY_FUT_df = filtered_NFO_BANKNIFTY_FUT_df.sort_values(by='Expiry')
    # print("line 123 : sorted NIFTY futidx \n", Sorted_filtered_NFO_BANKNIFTY_FUT_df)
    
    NIFTY_FUT_tkn_series = Sorted_filtered_NFO_NIFTY_FUT_df['Token']
    NIFTY_FUT_tradingsymbol_series = Sorted_filtered_NFO_NIFTY_FUT_df['TradingSymbol']
    NIFTY_FUT_tkn = NIFTY_FUT_tkn_series.iloc[0]
    NIFTY_FUT_TradingSymbol=NIFTY_FUT_tradingsymbol_series.iloc[0]
    
    BANKNIFTY_FUT_tkn_series = Sorted_filtered_NFO_BANKNIFTY_FUT_df['Token']
    BANKNIFTY_FUT_tradingsymbol_series = Sorted_filtered_NFO_BANKNIFTY_FUT_df['TradingSymbol']
    BANKNIFTY_FUT_tkn = BANKNIFTY_FUT_tkn_series.iloc[0]
    BANKNIFTY_FUT_TradingSymbol=BANKNIFTY_FUT_tradingsymbol_series.iloc[0]
    
    # print(" @ line 137 \n BANKNIFTY_FUT_TradingSymbol ", BANKNIFTY_FUT_TradingSymbol ," BANKNIFTY_FUT_tkn " , BANKNIFTY_FUT_tkn ,"\n",
            # " NIFTY_FUT_TradingSymbol " , NIFTY_FUT_TradingSymbol , " NIFTY_FUT_tkn " , NIFTY_FUT_tkn )
    
    del Sorted_filtered_NFO_NIFTY_FUT_df, NFO_NIFTY_FUT_boolean_mask ,filtered_NFO_NIFTY_FUT_df, NFO_BANKNIFTY_FUT_boolean_mask 
    del filtered_NFO_BANKNIFTY_FUT_df , Sorted_filtered_NFO_BANKNIFTY_FUT_df , NIFTY_FUT_tkn_series , NIFTY_FUT_tradingsymbol_series
    del BANKNIFTY_FUT_tkn_series , BANKNIFTY_FUT_tradingsymbol_series
    '''
    print(""" -------> starting from here code for selecting the options strike price 
            based on the indexs current as of now spot price aganist which below code is run
            and ATM options CE and PE strike prices are selected """)
    
    print(""" IMP Note : Key note :: indexes run indefinitely and stoks , while futures and options run with specific start and end dates 
            Run below paper trads , during all the below Code for exit trade if entered options Thetà , gamma or Vega , delta less than a specific value and trade is unfavourable condition 
            and opposite trade of ce or pe is expanding heavily To implement above see videos of 
            
            vix
            (https://www.youtube.com/shorts/OLaO3wj4kHs?feature=share , https://www.youtube.com/shorts/OLaO3wj4kHs,
            https://www.youtube.com/shorts/rkFPk-HJAlw?feature=share , https://www.youtube.com/shorts/rkFPk-HJAlw )
            
            visit india vix at 9.8 am in the morning
            take the previous days closing value of vix and divide it by sqroot of 365 = 19.1 and the result will 
            be equal to the todays market  up or down , check this for nifty 50 and banknifty,
            rupee to dollar and option greeks
            Code for always checking ce and pe opposite greeks and price change stagnation for exit of current Trade
            india vix basics and relation to options: 
            
            1#increase in india vix mean increases volatality in index, can go any side drastically mostly opposite of vix
            
            2#resulting in high option premiums and high time decay
            
            3# india vix prediction ?? "visit india vix at 9.8 am in the morning take the previous days closing value of vix 
            and divide it by sqroot of 365 = 19.1 and the result will be equal to the todays market up or down , 
            check this for nifty 50 and banknifty refer youtube [https://www.youtube.com/shorts/YWtP4BV1bIw?feature=share 
            or https://www.youtube.com/shorts/YWtP4BV1bIw]
            
            4# ****  India vix  if above 12 then only will be trending in any direction else will be  in side ways , 
            so  so write code to constantly check vix ( can subscribe? ), before entering or exiting trade do check the current value of the india vix so that to avoid trade 
            entries in sideways market https://www.youtube.com/shorts/ccxQ5gUsL1U or 
            https://www.youtube.com/shorts/ccxQ5gUsL1U?feature=share
            
            5# When india vix increased by nearly 10 % ( 7.3%) in below case and index went down buy PE instead of selling CE (basically india vix and index are moving in opposite direction) and vice versa 
            But if both india vix and indexes are moving in same direction, then avoid entering the trade as this may be pahse for market correction and subsequent stabilization
            refer https://www.youtube.com/shorts/_iipu_E268o or https://www.youtube.com/shorts/_iipu_E268o?feature=share
            
            6# India vix range per year  caliculation,but india vix itself changes every second in the same session,
            if india vix is 20 and index is 18000 upper range is index value * 120 and 
            lower range is index value * 80 for the year at that moment of time 
            https://www.youtube.com/shorts/PIKa8Mqq5gA or https://www.youtube.com/shorts/PIKa8Mqq5gA?feature=share
            
            7# if india vix is above 25 and index is going in oppsite directions beware that market can crash 
            https://www.youtube.com/shorts/ntrqs4KXT5U
            
            8#When india vix below 15 avoid option buying as index may go side ways and if india vix is above 25 avoid option selling 
            https://www.youtube.com/shorts/oRu5XjE3WE4?feature=share  or  https://www.youtube.com/shorts/oRu5XjE3WE4"
            
            1# option based on index ,
            2# based on index's weekly futures alone ,
            3# options via stocks: consider index's comprsing stocks and their percentage composition and contribution applicable for banknifty,
            4# options via weekly futures of stocks: take into account weekly futures of participating stocks in index consider percentage 
            composition and contribution of the relavant socks applicable for banknifty,
            4# weekly futures alone,
            3# based on option chart alone
            Target profit and cutt off loss to be set based on indicators combinations dynamically  than static profit loss percentage
            Also start plotting and saving graphsfrom first live paper trade
            Get banknifty futures data to see volume data """)   '''     
    return (NSE_NIFTY_tkn, NSE_NIFTY_TradingSymbol ,NSE_BANKNIFTY_tkn, NSE_BANKNIFTY_TradingSymbol,NIFTY_FUT_tkn , NIFTY_FUT_TradingSymbol , BANKNIFTY_FUT_tkn, BANKNIFTY_FUT_TradingSymbol)

def get_index_options():
    exch='NFO'
    # Symbol='NIFTY'
    symbol_df = pd.read_csv(f'https://api.shoonya.com/{exch}_symbols.txt.zip')
    symbol_df['Expiry'] = pd.to_datetime(symbol_df['Expiry']).apply(lambda x: x.date())
    # print('symbol_df : ', symbol_df)
    idx_df_banknifty= symbol_df[ (symbol_df.Symbol == 'BANKNIFTY' )]
    idx_df_nifty= symbol_df[ (symbol_df.Symbol == 'NIFTY' )]
    return idx_df_banknifty,idx_df_nifty

lastday=datetime.datetime.today()
# print('type(lastday) : ', type(lastday))
ist = pytz.timezone('Asia/Kolkata')
startdate=datetime.datetime(2000,1,1,9,15,0,tzinfo=ist)
startdate_time=startdate.timestamp()

lastday_timestamp = lastday.timestamp()

# ret3 =api.get_time_price_series( exchange='NSE',token='26009',starttime=startdate_time,endtime=lastday_timestamp,interval='5') 

# print('time_price_series : ' , ret3)

# print('\n option chain : ', api.get_option_chain(exchange='NSE',tradingsymbol='NIfty Bank',count=4,strikeprice='0') )

'''print("\n -------------> @line 242-294 code to finding nearest option strike price STARTS here <---------------\n")   '''         

# banknifty_ce = idx_df_banknifty[(idx_df_banknifty.OptionType == 'CE')]
# print('\n banknifty_ce  : \n', banknifty_ce)

# print("\n at line 163 NSE_BANKNIFTY_tkn  " , NSE_BANKNIFTY_tkn , " type(NSE_BANKNIFTY_tkn)  " , type(NSE_BANKNIFTY_tkn))

""" ------ Note here for the below included commented code pass the indexes tkn and its trading symbol to get weekly 
wk52_h: 49974.75, wk52_l: 42105.40 , lp: 49142.15 , close todays till now close or yesterdays close ??c: 49281.80, 
todays = days  h: 49511.15, l: 49043.65, o: 49390.90 as of now

symbol_tkn=str(symbol_tkn)
print(" symbol_tkn , TradingSymbol ",symbol_tkn,TradingSymbol)"""
# print("TradingSymbol and type of TradingSymbol is ",TradingSymbol,"  " , type(TradingSymbol))

# print('@ line 66  token  \n ', symbol_tkn, type(symbol_tkn), type(str(symbol_tkn)))

print(""" Below start date and end dates are caliculated and formed so that they can be used while calling the get time price series """)

StartBusday = (datetime.datetime.today() - timedelta(days=1)).replace(hour=9, minute=0, second=0, microsecond=0)
# today=datetime.datetime.today()
# print("StartBusday line 107",StartBusday)
StartBusday_1 = datetime.datetime.today() - timedelta(days=10)
EndBusDay = datetime.datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
EndBusDay_1 = datetime.datetime.today()

print("Start Bus day:", StartBusday, "End Bus Day:", EndBusDay)
print("Start Bus day 1:", StartBusday_1, "End Bus Day 1:", EndBusDay_1)

EndBusDay_timestamp = int(EndBusDay.timestamp())
StartBusday_timestamp = int(StartBusday.timestamp())
print(f" \n copy the below extracted values from dict of response of get_qoutes method wk52_h: 49974.75, wk52_l: 42105.40,lp: 49142.15,c: 49281.80, h: 49511.15, l: 49043.65, o: 49390.90 \n ")

# del resp_getQuotes
print("""get_time price series only gives info from the latest start of the current or closed @GENERAL TRADING session
      BETWEEN 9:15 TO 3.30 PM , COVERING THE START TIME AS 9:15 AND END TIME AS 3:30 PM converting data based on the interval choosen""")

print(""" Note : get_ time price series always gives the data backward from 
      current begining's last start and close of the given interval for
      example if you choose 5 min interval 15:25 or 3:25 pm as start and going back ward \n""")

print(""" note : get_time price series : if  interval is choosen as 15 mins and
      method is run at 4 pm  the first dict that will be returned starts from 15:15 / 3:15 pm as its completons ends at 15:30 or 3:30 pm
      and will go down back wards every 15 mins  """)
# print(' line 1119 === api.get_time_price_series(exchange=exch_NFO,token=ret_token)', 
#       api.get_time_price_series(exchange=search_exch, token=symbol_tkn ,interval=1, starttime=StartBusday_timestamp), '\n')
# print('999 api.get_daily_price_series', api.get_daily_price_series(exchange=search_exch, tradingsymbol=TradingSymbol, startdate=StartBusday_timestamp, enddate=EndBusDay_timestamp), '\n')

EndBusDay_1_timestamp = int(EndBusDay_1.timestamp())
StartBusday_1_timestamp = int(StartBusday_1.timestamp())
print("StartBusday_1_timestamp:", StartBusday_1_timestamp, type(StartBusday_1_timestamp), "EndBusDay_1_timestamp:", EndBusDay_1_timestamp, type(StartBusday_1_timestamp))
print("tradingsymbol=TradingSymbol", "TradingSymbol", "tradingsymbol=TradingSymbol", "TradingSymbol")

# del search_Symbol
# del search_exch

def unix_to_windows_time(unix_timestamp):
    # Define the start of the Windows file time epoch in Unix time
    windows_epoch_start = datetime.datetime(1601, 1, 1, 0, 0, 0)
    unix_epoch_start = datetime.datetime(1970, 1, 1, 0, 0, 0)

    # Calculate the difference in seconds between the two epochs
    epoch_difference_seconds = (unix_epoch_start - windows_epoch_start).total_seconds()

    # Calculate the Windows file time
    windows_file_time = (unix_timestamp + epoch_difference_seconds) * 10000000
    return int(windows_file_time)

# Example usage
unix_timestamp = 1716898273
# windows_file_time = unix_to_windows_time(unix_timestamp)
# print(windows_file_time)

def windows_to_unix_time(windows_file_time):
    # Define the start of the Windows file time epoch in Unix time
    windows_epoch_start = datetime.datetime(1601, 1, 1, 0, 0, 0)
    unix_epoch_start = datetime.datetime(1970, 1, 1, 0, 0, 0)

    # Calculate the difference in seconds between the two epochs
    epoch_difference_seconds = (unix_epoch_start - windows_epoch_start).total_seconds()

    # Convert the Windows file time from 100-nanosecond intervals to seconds
    unix_timestamp = (windows_file_time / 10000000) - epoch_difference_seconds
    return int(unix_timestamp)

# Example usage
windows_file_time = 133451948730000000
# unix_timestamp = windows_to_unix_time(windows_file_time)
# print(unix_timestamp)

print(""" ***** Checked Done this in the Live Market tomorrow ---->  if subscribing to the instrument or trading symbol , 
      there is no need to run the get_quote aditionally as the subscribe() below are today's level till now , so comment 
      out the variable saved from the get quotes and extract below mentioned variable values from dict output of the subscribe
and save the values from the out put of the subscribe() method like and 
*** call get Quotes only if the web socket failure or delay in subscribe method failure 
note: days Open price is the open of pre market hrs generally after 9 am and before 9:15 am (applicable for both get_quotes and subscribe)
h		days High price
l		days Low price
c		days Close price
above ends today's level

below starts the current sessions latest traded data
ft		Feed time
lp		latest LTP
pc		Percentage change from previous to latest ltp
v		volume
ap		Average trade price
ltt		Last trade time
ltq		Last trade quantity
tbq		Total Buy Quantity
tsq		Total Sell Quantity
sq1		Best Sell Quantity 1
sq2		Best Sell Quantity 2
above ends current sessions latest traded data

OI data in case of options
oi		Open interest
poi		Previous day closing Open Interest
toi		Total open interest for underlying
""")
api = NorenApi()
# api=ShoonyaApiPy()
api.set_session(userid=user_id,password=user_pwd,usertoken=login_token)
# api.token_setter(login_token)

(NSE_NIFTY_tkn, NSE_NIFTY_TradingSymbol ,NSE_BANKNIFTY_tkn, NSE_BANKNIFTY_TradingSymbol,NIFTY_FUT_tkn 
 , NIFTY_FUT_TradingSymbol , BANKNIFTY_FUT_tkn, BANKNIFTY_FUT_TradingSymbol) = (get_NSE_IDX_NFO_FUT())

while True:
    
    print(""" **** so save the O,H, L,C  recived from get_Quotes recieved in begining of last trading session 
          to compare aganist todays,this will help analyze morning trend that is about to happen in addition to 
          other data like previous days OHLC and CPR etc \n""")
    ret_idx_df_banknifty , ret_idx_df_nifty  =  get_index_options()
    # print('\n ret_idx_df_banknifty \n', ret_idx_df_banknifty)
    # print('\n ret_idx_df_banknifty \n', ret_idx_df_nifty)

    banknifty_ce = ret_idx_df_banknifty[ (ret_idx_df_banknifty.OptionType == 'CE') ]

    banknifty_pe = ret_idx_df_banknifty[ (ret_idx_df_banknifty.OptionType == 'PE') ]

    nifty_ce = ret_idx_df_nifty[ (ret_idx_df_nifty.OptionType == 'CE') ]

    nifty_pe = ret_idx_df_nifty[ (ret_idx_df_nifty.OptionType == 'PE') ]

    print("api.get_daily_price_series(NSE_BANKNIFTY_TradingSymbol)  bank nifty index " , api.get_daily_price_series(tradingsymbol=NSE_BANKNIFTY_TradingSymbol,exchange='NSE'))
    
    print("api.get_daily_price_series(NFO_BANKNIFTY_FUT_TradingSymbol)  bank nifty future " , api.get_daily_price_series(tradingsymbol=BANKNIFTY_FUT_TradingSymbol,exchange='NFO'))
    
    INDEX_BANKNIFTY_Quote=api.get_quotes(exchange='NSE',token=str(NSE_BANKNIFTY_tkn) )
    print ("\n get quote bank nifty index " , INDEX_BANKNIFTY_Quote)
    
    INDEX_BANKNIFTY_TimePriceSeries=api.get_time_price_series( exchange='NSE',token=str(NSE_BANKNIFTY_tkn),interval=5 )
    
    print ("\n INDEX_BANKNIFTY_TimePriceSeries  " , INDEX_BANKNIFTY_TimePriceSeries)
    
    FUT_BANKNIFTY_Quote=api.get_quotes(exchange='NFO',token=str(BANKNIFTY_FUT_tkn) )
    print ("\n FUT_BANKNIFTY_Quote  " , FUT_BANKNIFTY_Quote)
    
    FUT_BANKNIFTY_TimePriceSeries=api.get_time_price_series( exchange='NFO',token=str(BANKNIFTY_FUT_tkn),interval=5 )
    
    print ("\n FUT_BANKNIFTY_TimePriceSeries  " , FUT_BANKNIFTY_TimePriceSeries)
    
    banknifty_indx_lp = INDEX_BANKNIFTY_Quote['lp']
    banknifty_spot_price = float(banknifty_indx_lp)
    print("\n  Note : get quotes method returns LTP of extended pre and post market hours ")
    print('\n banknifty_spot_price : ', banknifty_spot_price ,'\n')

    banknifty_ce['Strike_Difference'] = abs(banknifty_ce['StrikePrice'] - banknifty_spot_price)
    banknifty_pe['Strike_Difference'] = abs(banknifty_pe['StrikePrice'] - banknifty_spot_price)

    # Find the CE strike price with the minimum difference
    banknifty_ce_closest_strike = (banknifty_ce.loc[banknifty_ce['Strike_Difference'].idxmin()]).to_dict()
    """
    print("\n banknifty Closest ATM  'CE' options:", banknifty_ce_closest_strike ,"  ", type(banknifty_ce_closest_strike),'\n')
    print("\n banknifty Closest ATM strike price for 'CE' options:", banknifty_ce_closest_strike['StrikePrice'] ,'\n')"""
    banknifty_ce_closest_strike_TradingSymbol=banknifty_ce_closest_strike['TradingSymbol'] 
    print("\n banknifty Closest ATM Trading Symbol for 'CE' options:", banknifty_ce_closest_strike_TradingSymbol ,'\n')
    banknifty_ce_closest_opt_quote = api.get_quotes('NFO', str(banknifty_ce_closest_strike['Token']))
    print('\n banknifty_ce_closest_opt_quote : \n ', banknifty_ce_closest_opt_quote) 
    
    # Find the PE strike price with the minimum difference
    banknifty_pe_closest_strike = (banknifty_pe.loc[banknifty_pe['Strike_Difference'].idxmin()]).to_dict()
    """
    print("\n Closest ATM  'PE' options:", banknifty_pe_closest_strike ,"  ", type(banknifty_pe_closest_strike),'\n')
    print("\n Closest ATM strike price for 'PE' options:", banknifty_pe_closest_strike['StrikePrice'] ,'\n')"""
    banknifty_pe_closest_strike_TradingSymbol=banknifty_pe_closest_strike['TradingSymbol'] 
    print("\n banknifty Closest ATM Trading Symbol for 'PE' options:", banknifty_pe_closest_strike_TradingSymbol ,'\n')
    banknifty_pe_closest_opt_quote = api.get_quotes('NFO', str(banknifty_pe_closest_strike['Token']))
    print('\n banknifty_pe_closest_opt_quote : \n ', banknifty_pe_closest_opt_quote) 
            
    idx_BNKNIFTY_wk52_h= INDEX_BANKNIFTY_Quote['wk52_h']
    idx_BNKNIFTY_wk52_l= INDEX_BANKNIFTY_Quote['wk52_l']
    idx_BNKNIFTY_quote_ltp= INDEX_BANKNIFTY_Quote['lp']
    idx_BNKNIFTY_Quote_close= INDEX_BANKNIFTY_Quote['c']
    idx_BNKNIFTY_Days_High_TillNow= INDEX_BANKNIFTY_Quote['h']
    idx_BNKNIFTY_Days_Low_TillNow= INDEX_BANKNIFTY_Quote['l']
    idx_BNKNIFTY_Quote_DaysOpen= INDEX_BANKNIFTY_Quote['o']
    idx_BNKNIFTY_Quote_request_time= INDEX_BANKNIFTY_Quote['request_time']

    print("idx_BNKNIFTY_Quote_request_time  , idx_BNKNIFTY_quote_ltp", idx_BNKNIFTY_Quote_request_time , ' ' , idx_BNKNIFTY_quote_ltp ,'\n')
    
    print("api.get_daily_price_series(NFO_NIFTY_FUT_TradingSymbol)  nifty future " , api.get_daily_price_series(tradingsymbol=NIFTY_FUT_TradingSymbol,exchange='NFO'))
    
    INDEX_NIFTY_Quote=api.get_quotes(exchange='NSE',token=str(NSE_NIFTY_tkn) )
    print ("\n get quote nifty index " , INDEX_NIFTY_Quote)
    
    INDEX_NIFTY_TimePriceSeries=api.get_time_price_series( exchange='NSE',token=str(NSE_NIFTY_tkn),interval=5 )
    
    print ("\n INDEX_NIFTY_TimePriceSeries  " , INDEX_NIFTY_TimePriceSeries)
    
    FUT_NIFTY_Quote=api.get_quotes(exchange='NFO',token=str(NIFTY_FUT_tkn) )
    print ("\n FUT_NIFTY_Quote  " , FUT_NIFTY_Quote)
    
    FUT_NIFTY_TimePriceSeries=api.get_time_price_series( exchange='NFO',token=str(NIFTY_FUT_tkn),interval=5 )
    
    print ("\n FUT_NIFTY_TimePriceSeries  " , FUT_NIFTY_TimePriceSeries)
    
    nifty_indx_lp = INDEX_NIFTY_Quote['lp']
    nifty_spot_price = float(nifty_indx_lp)
    print("\n Note : get quotes method returns LTP of extended pre and post market hours ")

    print('\n nifty_spot_price : ', nifty_spot_price ,'\n')

    nifty_ce['Strike_Difference'] = abs(nifty_ce['StrikePrice'] - nifty_spot_price)
    nifty_pe['Strike_Difference'] = abs(nifty_pe['StrikePrice'] - nifty_spot_price)  
    # Find the CE strike price with the minimum difference
    
    nifty_ce_closest_strike = (nifty_ce.loc[nifty_ce['Strike_Difference'].idxmin()]).to_dict()
    """
    print("\n nifty Closest ATM  'CE' options:", nifty_ce_closest_strike ,"  ", type(nifty_ce_closest_strike),'\n')
    print("\n nifty Closest ATM strike price for 'CE' options:", nifty_ce_closest_strike['StrikePrice'] ,'\n')"""
    banknifty_ce_closest_strike_TradingSymbol=banknifty_ce_closest_strike['TradingSymbol'] 
    print("\n banknifty Closest ATM Trading Symbol for 'CE' options:", banknifty_ce_closest_strike_TradingSymbol ,'\n')
    nifty_ce_closest_opt_quote = api.get_quotes('NFO', str(nifty_ce_closest_strike['Token']))
    print('\n nifty_ce_closest_opt_quote : \n ', nifty_ce_closest_opt_quote) 
    
    # Find the PE strike price with the minimum difference
    nifty_pe_closest_strike = (nifty_pe.loc[nifty_pe['Strike_Difference'].idxmin()]).to_dict()
    """print("\n Closest ATM  'PE' options:", nifty_pe_closest_strike ,"  ", type(nifty_pe_closest_strike),'\n')
    print("\n Closest ATM strike price for 'PE' options:", nifty_pe_closest_strike['StrikePrice'] ,'\n')"""
    nifty_pe_closest_strike_TradingSymbol=nifty_pe_closest_strike['TradingSymbol'] 
    print("\n nifty Closest ATM Trading Symbol for 'PE' options:", nifty_pe_closest_strike_TradingSymbol ,'\n')
    nifty_pe_closest_opt_quote = api.get_quotes('NFO', str(nifty_pe_closest_strike['Token']))
    print('\n nifty_pe_closest_opt_quote : \n ', nifty_pe_closest_opt_quote) 
            
    idx_NIFTY50_wk52_h= INDEX_NIFTY_Quote['wk52_h']
    idx_NIFTY50_wk52_l= INDEX_NIFTY_Quote['wk52_l']
    idx_NIFTY50_quote_ltp= INDEX_NIFTY_Quote['lp']
    idx_NIFTY50_Quote_close= INDEX_NIFTY_Quote['c']
    idx_NIFTY50_Days_High_TillNow= INDEX_NIFTY_Quote['h']
    idx_NIFTY50_Days_Low_TillNow= INDEX_NIFTY_Quote['l']
    idx_NIFTY50_Quote_DaysOpen= INDEX_NIFTY_Quote['o']
    idx_NIFTY50_Quote_request_time= INDEX_NIFTY_Quote['request_time']

    print("\n idx_NIFTY50_Quote_request_time  , idx_NIFTY50_quote_ltp", idx_NIFTY50_Quote_request_time , ' ' , idx_NIFTY50_quote_ltp ,'\n')
    
    # ret = api.option_greek(expiredate ='24-NOV-2022',StrikePrice='150',SpotPrice  = '200',InterestRate  = '100',Volatility = '10',OptionType='5')
    # ret = api.option_greek(expiredate ='20-JUN-2024',StrikePrice='150',SpotPrice  = '200',InterestRate  = '100',Volatility = '10',OptionType='CE')
    # apiret = api.option_greek(expiredate ='24-NOV-2022',StrikePrice='150',SpotPrice  = '200',InitRate  = '100',Volatility = '10',OptionType='CE')
   
    sleep(60)