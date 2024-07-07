import pandas as pd
from datetime import datetime, timedelta
import random
import time
import os

class currentdaysOHLC:
    # Simulate continuous data feed of LTP
    # def ltp_data_feed():
    #     while True:
    #         # Simulate the current time and LTP
    #         current_time = datetime.now()
    #         ltp = random.uniform(100, 200)  # Random LTP between 100 and 200
    #         yield current_time, ltp
    #         time.sleep(1)  # Simulate data feed with a delay of 1 second
    days_ohlc_sofar = {
        'Start Time': None,
        'End Time': None,
        'Open': None,
        'High': None,
        'Low': None,
        'Close': None
    }
    def __init__(self, ltp, tkn, symbol,timeframefile):
        self.ltp=ltp
        self.tkn=tkn
        self.symbol=symbol
        self.timeframefile=timeframefile
        
    
    # Function to align to the start of the next minute
    def align_to_minute_start(self):
        current_time = datetime.now()
        return current_time.replace(second=0, microsecond=0) + timedelta(minutes=1)

    # Function to read the time frame from a file
    def read_time_frame(self,timeframefile):
        with open(timeframefile, 'r') as file:
            time_frame = int(file.read().strip())
        return time_frame

    # Global dictionary to store current day's OHLC data
    

    # Function to aggregate LTP data into OHLC
    def aggregate_ohlc(data_feed, file_path):
        # Dictionary to store current time frame OHLC data
        ohlc_data = {
            'Start Time': None,
            'End Time': None,
            'Open': None,
            'High': None,
            'Low': None,
            'Close': None
        }
        
        # Variables to store current period data
        open_price = high_price = low_price = close_price = None
        
        # Get the initial time frame and start time
        time_frame = read_time_frame(file_path)
        current_period_start = align_to_minute_start(datetime.now())
        next_period_start = current_period_start + timedelta(minutes=time_frame)
        
        for current_time, ltp in data_feed:
            new_time_frame = read_time_frame(file_path)
            if new_time_frame != time_frame:
                time_frame = new_time_frame
                next_period_start = current_period_start + timedelta(minutes=time_frame)
            
            if current_time >= next_period_start:
                # Update the OHLC data for the completed period
                ohlc_data['Start Time'] = current_period_start
                ohlc_data['End Time'] = next_period_start - timedelta(seconds=1)
                ohlc_data['Open'] = open_price
                ohlc_data['High'] = max(high_price, days_ohlc_sofar['High']) if days_ohlc_sofar['High'] is not None else high_price
                ohlc_data['Low'] = min(low_price, days_ohlc_sofar['Low']) if days_ohlc_sofar['Low'] is not None else low_price
                ohlc_data['Close'] = close_price
                
                # Update the day's OHLC data
                update_days_ohlc(ohlc_data)
                
                # Return the OHLC data for the completed period
                yield ohlc_data
                
                # Start a new period
                current_period_start = next_period_start
                next_period_start = current_period_start + timedelta(minutes=time_frame)
                open_price = high_price = low_price = close_price = ltp
            else:
                # Update high, low, and close prices within the same period
                if open_price is None:
                    open_price = ltp
                high_price = max(high_price, ltp) if high_price is not None else ltp
                low_price = min(low_price, ltp) if low_price is not None else ltp
                close_price = ltp
            
            # Update the current OHLC data
            ohlc_data['Start Time'] = current_period_start
            ohlc_data['End Time'] = next_period_start - timedelta(seconds=1)
            ohlc_data['Open'] = open_price
            ohlc_data['High'] = high_price
            ohlc_data['Low'] = low_price
            ohlc_data['Close'] = close_price

    # Function to update the current day's OHLC data
    def update_days_ohlc(self,ohlc_data):
        global days_ohlc_sofar
        # Always update Open with initial value, Close with latest value
        if days_ohlc_sofar['Open'] is None:
            days_ohlc_sofar['Open'] = ohlc_data['Open']
            days_ohlc_sofar['High'] = ohlc_data['High']
            days_ohlc_sofar['Low'] = ohlc_data['Low']
        # days_ohlc_sofar['High'] = max(days_ohlc_sofar['High'], ohlc_data['High']) if days_ohlc_sofar['High'] is not None else ohlc_data['High']
        # days_ohlc_sofar['Low'] = min(days_ohlc_sofar['Low'], ohlc_data['Low']) if days_ohlc_sofar['Low'] is not None else ohlc_data['Low']
        # days_ohlc_sofar['Close'] = ohlc_data['Close']
        days_ohlc_sofar['High'] = max(days_ohlc_sofar['High'], ohlc_data['High'])
        days_ohlc_sofar['Low'] = min(days_ohlc_sofar['Low'], ohlc_data['Low'])
        days_ohlc_sofar['Close'] = ohlc_data['Close']

    # Example usage
    file_path = r'C:\Users\GovardhanLaptop\Downloads\Shoonya_NEW-20240205T090853Z-001\Shoonya_NEW\GovAutoTradingTestCode\candle_timeFrame.txt'
    data_feed = ltp_data_feed()
    ohlc_generator = aggregate_ohlc(data_feed, file_path)

    for ohlc_data in ohlc_generator:
        print(f"Start Time: {ohlc_data['Start Time']}, End Time: {ohlc_data['End Time']}, Open: {ohlc_data['Open']}, High: {ohlc_data['High']}, Low: {ohlc_data['Low']}, Close: {ohlc_data['Close']}")
        print(f"Current Day's OHLC: {days_ohlc_sofar}")
