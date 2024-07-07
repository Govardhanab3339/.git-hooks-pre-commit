import pandas as pd
from datetime import datetime, timedelta
from NorenApi import NorenApi

# Initialize API
api = NorenApi()

user_id = 'FA108224'
user_pwd = 'Ram39#Kils'
token = open("shoonyakey.txt", 'r').read().strip()
api.set_session(userid=user_id, password=user_pwd, usertoken=token)

# Set start_time to the beginning of today
start_time = datetime.today()
start_time = start_time.replace(hour=0, minute=0, second=0, microsecond=0)

# Convert start_time and end_time to Unix timestamps
start_time_unix = int(start_time.timestamp())
# end_time = start_time - timedelta(days=1)
# end_time_unix = int(end_time.timestamp())

# Fetch data
data = pd.DataFrame(api.get_time_price_series(exchange='NSE', token='26000', starttime=start_time_unix, interval=5))

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

# Check if the current time is after 3:30 PM
current_time = datetime.now()
if current_time.hour > 15 or (current_time.hour == 15 and current_time.minute > 30):
    previous_date = most_recent_date
    previous_date_data = recent_date_data

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
