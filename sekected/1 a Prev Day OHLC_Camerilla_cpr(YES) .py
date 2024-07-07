import pandas as pd
from datetime import datetime,timedelta
from NorenApi import NorenApi

# # Example data for demonstration purposes
# data = pd.DataFrame([
#     {'stat': 'Ok', 'time': '18-06-2024 15:25:00', 'ssboe': '1718704500', 'into': '23565.45', 'inth': '23572.10', 'intl': '23558.05', 'intc': '23562.30', 'intvwap': '0.00', 'intv': '0', 'intoi': '0', 'v': '0', 'oi': '0'},
#     {'stat': 'Ok', 'time': '18-06-2024 15:20:00', 'ssboe': '1718704200', 'into': '23561.80', 'inth': '23567.90', 'intl': '23559.05', 'intc': '23565.60', 'intvwap': '0.00', 'intv': '0', 'intoi': '0', 'v': '0', 'oi': '0'},
#     {'stat': 'Ok', 'time': '17-06-2024 15:25:00', 'ssboe': '1718618100', 'into': '23455.45', 'inth': '23462.10', 'intl': '23448.05', 'intc': '23452.30', 'intvwap': '0.00', 'intv': '0', 'intoi': '0', 'v': '0', 'oi': '0'},
#     {'stat': 'Ok', 'time': '17-06-2024 15:20:00', 'ssboe': '1718617800', 'into': '23451.80', 'inth': '23457.90', 'intl': '23449.05', 'intc': '23455.60', 'intvwap': '0.00', 'intv': '0', 'intoi': '0', 'v': '0', 'oi': '0'},
#     # Additional data entries...
# ])

api=NorenApi()

api.exit_order(orderno='', product_type='')

user_id    = 'FA108224'
user_pwd     = 'Ram39#Kils'
# api = NorenApi()
# factor2 = pyotp.TOTP('EETL2QPZ63D25PBN4564T6526R34I77Q').now()  # This should be TOTP
# vc      = 'FA108224_U'
# app_key = 'df41b1771499934e366634c53f19ac3f'
# imei    = 'abc1234'
# accesstoken = ''

token = open("shoonyakey.txt",'r').read().strip()

api.set_session(userid=user_id,password=user_pwd ,usertoken=token)

# start_time = datetime.today()
# start_time = start_time.replace(hour=0, minute=0, second=0, microsecond=0)

# # starttime = datetime.datetime.today()
# end_time = start_time-timedelta(days=1, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0)

# data = pd.DataFrame(api.get_time_price_series(exchange='NSE',token='26000',interval=5 , starttime=start_time , endtime=end_time ))  

# print("data " , data)

from datetime import datetime, timedelta
import pandas as pd

# Set start_time to the beginning of today
Towards_todays_Datetime = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
Towards_todays_Datetime_unix = int(Towards_todays_Datetime.timestamp())
Away_from_Todays_Datetime = Towards_todays_Datetime - timedelta(days=6)
Away_from_Todays_Datetime_unix = int(Away_from_Todays_Datetime.timestamp())

# Convert start_time and end_time to Unix timestamps
# start_time_unix = int(start_time.timestamp())

data =pd.DataFrame(api.get_time_price_series(exchange='NSE', token='26000', starttime=Away_from_Todays_Datetime_unix , endtime=Towards_todays_Datetime_unix  , interval=5))

print("data:", data)


# data= pd.DataFrame(data)
# print("\n data " , type(data))
# data = pd.DataFrame([
#     {'stat': 'Ok', 'time': '18-06-2024 15:25:00', 'ssboe': '1718704500', 'into': '23565.45', 'inth': '23572.10', 'intl': '23558.05', 'intc': '23562.30', 'intvwap': '0.00', 'intv': '0', 'intoi': '0', 'v': '0', 'oi': '0'},
#     {'stat': 'Ok', 'time': '18-06-2024 15:20:00', 'ssboe': '1718704200', 'into': '23561.80', 'inth': '23567.90', 'intl': '23559.05', 'intc': '23565.60', 'intvwap': '0.00', 'intv': '0', 'intoi': '0', 'v': '0', 'oi': '0'},
#     {'stat': 'Ok', 'time': '26-06-2024 15:25:00', 'ssboe': '1718618100', 'into': '23455.45', 'inth': '23462.10', 'intl': '23448.05', 'intc': '23452.30', 'intvwap': '0.00', 'intv': '0', 'intoi': '0', 'v': '0', 'oi': '0'},
#     {'stat': 'Ok', 'time': '26-06-2024 15:20:00', 'ssboe': '1718617800', 'into': '23451.80', 'inth': '23457.90', 'intl': '23449.05', 'intc': '23455.60', 'intvwap': '0.00', 'intv': '0', 'intoi': '0', 'v': '0', 'oi': '0'},
#     # Additional data entries...
# ])

# Convert 'time' column to datetime
data['datetime'] = pd.to_datetime(data['time'], format='%d-%m-%Y %H:%M:%S')

# Get the most recent date
most_recent_date = data['datetime'].dt.date.max()

# Filter data for the most recent date
recent_date_data = data[data['datetime'].dt.date == most_recent_date]

# Get the previous date
previous_date = (data['datetime'].dt.date[data['datetime'].dt.date < most_recent_date]).max()

# Filter data for the previous date
previous_date_data = data[data['datetime'].dt.date == previous_date]

print("previous_date_data " , previous_date_data)

# Calculate OHLC for the previous date


previous_date_open = round(float(previous_date_data.iloc[0]['into']), 2)
previous_date_high = round(float(previous_date_data['inth'].astype(float).max()), 2)
previous_date_low = round(float(previous_date_data['intl'].astype(float).min()), 2)
previous_date_close = round(float(previous_date_data.iloc[-1]['intc']), 2)

# previous_date_open = float(previous_date_data.iloc[0]['into'])
# previous_date_high = float(previous_date_data['inth'].astype(float).max())
# previous_date_low = float(previous_date_data['intl'].astype(float).min())
# previous_date_close = float(previous_date_data.iloc[-1]['intc'])

# # Calculate OHLC for the previous date
# previous_date_open = int(previous_date_data.iloc[0]['into'])
# previous_date_high = int(previous_date_data['inth'].astype(float).max())
# previous_date_low = int(previous_date_data['intl'].astype(float).min())
# previous_date_close = int(previous_date_data.iloc[-1]['intc'])

# Print the OHLC values
print(f"Previous Date: {previous_date}")
print(f"Previous Date ->  Open: {previous_date_open}, High: {previous_date_high}, Low: {previous_date_low}, Close: {previous_date_close}")

# Example function to calculate Camarilla pivot points
def calculate_camarilla_pivots( previous_date_high, previous_date_low, previous_date_close):
    range_ = previous_date_high - previous_date_low
    print(f"range_ , {type(range_)} , previous_date_close . {type(previous_date_close)} ")
    r4= round((previous_date_close + (range_ * 1.1 / 2)), 2)
    r3= round((previous_date_close + (range_ * 1.1 / 4)), 2)
    r2= round((previous_date_close + (range_ * 1.1 / 6)), 2)
    r1= round((previous_date_close + (range_ * 1.1 / 12)), 2)
    s1= round((previous_date_close - (range_ * 1.1 / 12)), 2)
    s2= round((previous_date_close - (range_ * 1.1 / 6)), 2)
    s3= round((previous_date_close - (range_ * 1.1 / 4)), 2)
    s4= round((previous_date_close - (range_ * 1.1 / 2)), 2)
    return  r4, r3, r2, r1, s1, s2, s3, s4


def calculate_cpr(previous_date_high, previous_date_low, previous_date_close):
    # previous_day = data.iloc[-1]  # Use the last entry in the historical data as the previous day
    pivot = round(((previous_date_high + previous_date_low + previous_date_close) / 3),2)
    bc = round(((previous_date_high + previous_date_low) / 2),2)
    tc = round((2 * pivot - bc),2)
    return pivot, bc, tc

# Calculate the Camarilla pivot points
camrila_r4, camrila_r3, camrila_r2, camrila_r1, camrila_s1, camrila_s2, camrila_s3, camrila_s4  = calculate_camarilla_pivots(previous_date_high, previous_date_low, previous_date_close)
print("\n camrila_r4, camrila_r3, camrila_r2, camrila_r1, camrila_s1, camrila_s2, camrila_s3, camrila_s4:", camrila_r4, camrila_r3, camrila_r2, camrila_r1, camrila_s1, camrila_s2, camrila_s3, camrila_s4)

cpr_pivot , cpr_bc, cpr_tc = calculate_cpr(previous_date_high, previous_date_low, previous_date_close)
print("\n cpr_pivot, cpr_bc, cpr_tc ", cpr_pivot, cpr_bc, cpr_tc )