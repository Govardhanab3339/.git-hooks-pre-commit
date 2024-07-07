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
        self.time_frame = self.read_time_frame()
        self.current_period_start = self.align_to_minute_start()
        self.next_period_start = self.current_period_start + timedelta(minutes=self.time_frame)
        self.open_price = self.high_price = self.low_price = self.close_price = None

    def align_to_minute_start(self):
        current_time = datetime.now()
        return current_time.replace(second=0, microsecond=0) + timedelta(minutes=1)

    def read_time_frame(self):
        with open(self.timeframefile, 'r') as file:
            time_frame = int(file.read().strip())
        return time_frame

    def aggregate_ohlc(self, current_time, ltp):
        new_time_frame = self.read_time_frame()
        if new_time_frame != self.time_frame:
            self.time_frame = new_time_frame
            self.next_period_start = self.current_period_start + timedelta(minutes=self.time_frame)

        if current_time >= self.next_period_start:
            ohlc_data = {
                'Start Time': self.current_period_start,
                'End Time': self.next_period_start - timedelta(seconds=1),
                'Open': self.open_price,
                'High': max(self.high_price, self.days_ohlc_sofar['High']) if self.days_ohlc_sofar['High'] is not None else self.high_price,
                'Low': min(self.low_price, self.days_ohlc_sofar['Low']) if self.days_ohlc_sofar['Low'] is not None else self.low_price,
                'Close': self.close_price
            }

            self.update_days_ohlc(ohlc_data)
            self.current_period_start = self.next_period_start
            self.next_period_start = self.current_period_start + timedelta(minutes=self.time_frame)
            self.open_price = self.high_price = self.low_price = self.close_price = ltp
            return ohlc_data
        else:
            if self.open_price is None:
                self.open_price = ltp
            self.high_price = max(self.high_price, ltp) if self.high_price is not None else ltp
            self.low_price = min(self.low_price, ltp) if self.low_price is not None else ltp
            self.close_price = ltp

    def update_days_ohlc(self, ohlc_data):
        if self.days_ohlc_sofar['Open'] is None:
            self.days_ohlc_sofar['Open'] = ohlc_data['Open']
            self.days_ohlc_sofar['High'] = ohlc_data['High']
            self.days_ohlc_sofar['Low'] = ohlc_data['Low']
        self.days_ohlc_sofar['High'] = max(self.days_ohlc_sofar['High'], ohlc_data['High'])
        self.days_ohlc_sofar['Low'] = min(self.days_ohlc_sofar['Low'], ohlc_data['Low'])
        self.days_ohlc_sofar['Close'] = ohlc_data['Close']

    def update_ltp(self, ltp):
        current_time = datetime.now()
        ohlc_data = self.aggregate_ohlc(current_time, ltp)
        if ohlc_data:
            print(f"Start Time: {ohlc_data['Start Time']}, End Time: {ohlc_data['End Time']}, Open: {ohlc_data['Open']}, High: {ohlc_data['High']}, Low: {ohlc_data['Low']}, Close: {ohlc_data['Close']}")
        print(f"Current Day's OHLC: {CurrentDaysOHLC.days_ohlc_sofar}")
