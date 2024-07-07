import pandas as pd
from datetime import datetime, timedelta
import random
import time
import os

class CurrentDaysOHLC:
    days_ohlc_sofar = {
        'Start Time': None,
        'End Time': None,
        'Open': None,
        'High': None,
        'Low': None,
        'Close': None
    }

    def __init__(self, ltp, tkn, symbol, timeframefile):
        self.ltp = ltp
        self.tkn = tkn
        self.symbol = symbol
        self.timeframefile = timeframefile

    def ltp_data_feed(self):
        while True:
            current_time = datetime.now()
            ltp = random.uniform(100, 200)
            yield current_time, ltp
            time.sleep(1)

    def align_to_minute_start(self):
        current_time = datetime.now()
        return current_time.replace(second=0, microsecond=0) + timedelta(minutes=1)

    def read_time_frame(self):
        with open(self.timeframefile, 'r') as file:
            time_frame = int(file.read().strip())
        return time_frame

    def aggregate_ohlc(self, data_feed):
        ohlc_data = {
            'Start Time': None,
            'End Time': None,
            'Open': None,
            'High': None,
            'Low': None,
            'Close': None
        }

        open_price = high_price = low_price = close_price = None
        time_frame = self.read_time_frame()
        current_period_start = self.align_to_minute_start()
        next_period_start = current_period_start + timedelta(minutes=time_frame)

        for current_time, ltp in data_feed:
            new_time_frame = self.read_time_frame()
            if new_time_frame != time_frame:
                time_frame = new_time_frame
                next_period_start = current_period_start + timedelta(minutes=time_frame)

            if current_time >= next_period_start:
                ohlc_data['Start Time'] = current_period_start
                ohlc_data['End Time'] = next_period_start - timedelta(seconds=1)
                ohlc_data['Open'] = open_price
                ohlc_data['High'] = max(high_price, self.days_ohlc_sofar['High']) if self.days_ohlc_sofar['High'] is not None else high_price
                ohlc_data['Low'] = min(low_price, self.days_ohlc_sofar['Low']) if self.days_ohlc_sofar['Low'] is not None else low_price
                ohlc_data['Close'] = close_price

                self.update_days_ohlc(ohlc_data)
                yield ohlc_data

                current_period_start = next_period_start
                next_period_start = current_period_start + timedelta(minutes=time_frame)
                open_price = high_price = low_price = close_price = ltp
            else:
                if open_price is None:
                    open_price = ltp
                high_price = max(high_price, ltp) if high_price is not None else ltp
                low_price = min(low_price, ltp) if low_price is not None else ltp
                close_price = ltp

            ohlc_data['Start Time'] = current_period_start
            ohlc_data['End Time'] = next_period_start - timedelta(seconds=1)
            ohlc_data['Open'] = open_price
            ohlc_data['High'] = high_price
            ohlc_data['Low'] = low_price
            ohlc_data['Close'] = close_price

    def update_days_ohlc(self, ohlc_data):
        if self.days_ohlc_sofar['Open'] is None:
            self.days_ohlc_sofar['Open'] = ohlc_data['Open']
            self.days_ohlc_sofar['High'] = ohlc_data['High']
            self.days_ohlc_sofar['Low'] = ohlc_data['Low']
        self.days_ohlc_sofar['High'] = max(self.days_ohlc_sofar['High'], ohlc_data['High'])
        self.days_ohlc_sofar['Low'] = min(self.days_ohlc_sofar['Low'], ohlc_data['Low'])
        self.days_ohlc_sofar['Close'] = ohlc_data['Close']

if __name__ == "__main__":
    file_path = r'C:\Users\GovardhanLaptop\Downloads\Shoonya_NEW-20240205T090853Z-001\Shoonya_NEW\GovAutoTradingTestCode\candle_timeFrame.txt'
    current_days_ohlc = CurrentDaysOHLC(None, None, None, file_path)
    data_feed = current_days_ohlc.ltp_data_feed()
    ohlc_generator = current_days_ohlc.aggregate_ohlc(data_feed)

    for ohlc_data in ohlc_generator:
        print(f"Start Time: {ohlc_data['Start Time']}, End Time: {ohlc_data['End Time']}, Open: {ohlc_data['Open']}, High: {ohlc_data['High']}, Low: {ohlc_data['Low']}, Close: {ohlc_data['Close']}")
        print(f"Current Day's OHLC: {CurrentDaysOHLC.days_ohlc_sofar}")
