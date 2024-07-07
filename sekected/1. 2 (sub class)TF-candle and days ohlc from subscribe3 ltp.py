from your_module import CurrentDaysOHLC
import random
import time

file_path = r'C:\Users\GovardhanLaptop\Downloads\Shoonya_NEW-20240205T090853Z-001\Shoonya_NEW\GovAutoTradingTestCode\candle_timeFrame.txt'
current_days_ohlc = CurrentDaysOHLC(None, None, None, file_path)

while True:
    ltp = random.uniform(100, 200)
    current_days_ohlc.update_ltp(ltp)
    print(f"Current Day's OHLC: {CurrentDaysOHLC.days_ohlc_sofar}")
    time.sleep(1)
