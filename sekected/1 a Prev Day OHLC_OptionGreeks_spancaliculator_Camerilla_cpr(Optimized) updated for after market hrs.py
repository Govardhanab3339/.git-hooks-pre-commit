import pandas as pd
from datetime import datetime, timedelta
from NorenApi import NorenApi

# Initialize API
api = NorenApi()

user_id = 'FA108224'
user_pwd = 'Ram39#Kils'
token = open("shoonyakey.txt", 'r').read().strip()
api.set_session(userid=user_id, password=user_pwd, usertoken=token)

print("""-->implement condition to get the prev days day level ohlc values using daily_price series
      if fail then check the time price series refer the word doc 
      'difference of result data by dailyPS and TimePS and Quote api methods.docx' for learning ,
      sample code run in the document is win the below code snippets
      about daily price series , time price series and the get quote 
      for prev day ohlc ,  cpr , camerilla<--""")

# Set start_time to the beginning of today
HistoricalLatest_EndDatetime = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
HistoricalLatest_EndDatetime_unix = int(HistoricalLatest_EndDatetime.timestamp())
HistoricalPrev_StartDatetime = HistoricalLatest_EndDatetime - timedelta(days=6)
HistoricalPrev_StartDatetime_unix = int(HistoricalPrev_StartDatetime.timestamp())

# HistoricalLatest_EndDatetime = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
# HistoricalLatest_EndDatetime_unix = int(HistoricalLatest_EndDatetime.timestamp())
# HistoricalPrev_StartDatetime = HistoricalLatest_EndDatetime - timedelta(days=6)
# HistoricalPrev_StartDatetime_unix = int(HistoricalPrev_StartDatetime.timestamp())

# Fetch data from the API
# data = pd.DataFrame(api.get_time_price_series(exchange='NSE', token='26000', starttime=start_time_unix,endtime=end_time_unix, interval=240))

data_daily =pd.DataFrame(api.get_daily_price_series(exchange='NSE',tradingsymbol='Nifty 50',startdate=HistoricalPrev_StartDatetime_unix , enddate=HistoricalLatest_EndDatetime_unix ))

data =pd.DataFrame(api.get_time_price_series(exchange='NSE', token='26000', starttime=HistoricalPrev_StartDatetime_unix , endtime=HistoricalLatest_EndDatetime_unix  , interval=5))


ret = api.option_greek(expiredate ='3-JUL-2024',StrikePrice='52200',SpotPrice  = '52168.1',InterestRate  = '.0701',Volatility = '0.1662594996250992',OptionType='CE')

print("option greek \n ", ret)

# data_df =pd.DataFrame(api.get_daily_price_series(exchange='NSE',tradingsymbol='Nifty 50'))
print ( '\n data_daily ' , api.get_daily_price_series(exchange='NSE',tradingsymbol='Nifty 50',startdate=HistoricalPrev_StartDatetime_unix , enddate=HistoricalLatest_EndDatetime_unix ) )

print("\n  quote nifty 50 ", api.get_quotes(exchange="NSE",token="26009",))
print("\n data_daily_DF ", data_daily)

print("\n data_tps", data)

# Convert 'time' column to datetime
data['datetime'] = pd.to_datetime(data['time'], format='%d-%m-%Y %H:%M:%S')

# Determine the most recent and previous dates
most_recent_date = data['datetime'].dt.date.max()
previous_date = (data['datetime'].dt.date[data['datetime'].dt.date < most_recent_date]).max()

time.sleep(.001)
# Check if the current time is after 3:30 PM
current_time = datetime.now()
# if current_time.hour > 15 or (current_time.hour == 15 and current_time.minute > 30):
#     previous_date = most_recent_date

# Filter data for the relevant dates
previous_date_data = data[data['datetime'].dt.date == previous_date]

# Calculate OHLC for the previous date
previous_date_open = round(float(previous_date_data.iloc[0]['into']), 2)
previous_date_high = round(float(previous_date_data['inth'].astype(float).max()), 2)
previous_date_low = round(float(previous_date_data['intl'].astype(float).min()), 2)
previous_date_close = round(float(previous_date_data.iloc[-1]['intc']), 2)

# Print the OHLC values
print(f"Previous Date: {previous_date}")
print(f"Previous Date -> Open: {previous_date_open}, High: {previous_date_high}, Low: {previous_date_low}, Close: {previous_date_close}")

# Example function to calculate Camarilla pivot points
def calculate_camarilla_pivots(previous_date_high, previous_date_low, previous_date_close):
    range_ = previous_date_high - previous_date_low
    r4 = round((previous_date_close + (range_ * 1.1 / 2)), 2)
    r3 = round((previous_date_close + (range_ * 1.1 / 4)), 2)
    r2 = round((previous_date_close + (range_ * 1.1 / 6)), 2)
    r1 = round((previous_date_close + (range_ * 1.1 / 12)), 2)
    s1 = round((previous_date_close - (range_ * 1.1 / 12)), 2)
    s2 = round((previous_date_close - (range_ * 1.1 / 6)), 2)
    s3 = round((previous_date_close - (range_ * 1.1 / 4)), 2)
    s4 = round((previous_date_close - (range_ * 1.1 / 2)), 2)
    return r4, r3, r2, r1, s1, s2, s3, s4

def calculate_cpr(previous_date_high, previous_date_low, previous_date_close):
    pivot = round(((previous_date_high + previous_date_low + previous_date_close) / 3), 2)
    bc = round(((previous_date_high + previous_date_low) / 2), 2)
    tc = round((2 * pivot - bc), 2)
    return pivot, bc, tc

# Calculate the Camarilla pivot points
camrila_r4, camrila_r3, camrila_r2, camrila_r1, camrila_s1, camrila_s2, camrila_s3, camrila_s4 = calculate_camarilla_pivots(previous_date_high, previous_date_low, previous_date_close)
print("\nCamarilla Pivots:", camrila_r4, camrila_r3, camrila_r2, camrila_r1, camrila_s1, camrila_s2, camrila_s3, camrila_s4)

cpr_pivot, cpr_bc, cpr_tc = calculate_cpr(previous_date_high, previous_date_low, previous_date_close)
print("\nCPR:", cpr_pivot, cpr_bc, cpr_tc)
