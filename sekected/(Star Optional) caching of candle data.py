import pandas as pd
import cachetools
import time
from cachetools import TTLCache
import hashlib

# Initialize a TTL cache with a max size of 100 and a TTL of 5 seconds
cache = TTLCache(maxsize=100, ttl=5)

def hash_candle(candle):
    candle_str = f"{candle['Open']}{candle['Close']}{candle['High']}{candle['Low']}"
    return hashlib.md5(candle_str.encode()).hexdigest()

def is_hammer(data):
    last_candle = data.iloc[-1]
    cache_key = (hash_candle(last_candle), 'is_hammer')
    if cache_key in cache:
        return cache[cache_key]
    
    body_size = abs(last_candle['Close'] - last_candle['Open'])
    lower_shadow = last_candle['Low'] - min(last_candle['Close'], last_candle['Open'])
    upper_shadow = last_candle['High'] - max(last_candle['Close'], last_candle['Open'])
    result = lower_shadow > 2 * body_size and upper_shadow < 0.1 * body_size
    cache[cache_key] = result
    return result

def is_shooting_star(data):
    last_candle = data.iloc[-1]
    cache_key = (hash_candle(last_candle), 'is_shooting_star')
    if cache_key in cache:
        return cache[cache_key]
    
    body_size = abs(last_candle['Close'] - last_candle['Open'])
    upper_shadow = last_candle['High'] - max(last_candle['Close'], last_candle['Open'])
    lower_shadow = min(last_candle['Close'], last_candle['Open']) - last_candle['Low']
    result = upper_shadow > 2 * body_size and lower_shadow < 0.1 * body_size
    cache[cache_key] = result
    return result

def is_bullish_abandoned_baby(data):
    if len(data) < 3:
        return False
    
    first_candle = data.iloc[-3]
    second_candle = data.iloc[-2]
    third_candle = data.iloc[-1]
    
    cache_key = (hash_candle(first_candle), hash_candle(second_candle), hash_candle(third_candle), 'is_bullish_abandoned_baby')
    if cache_key in cache:
        return cache[cache_key]
    
    is_bearish_first = first_candle['Close'] < first_candle['Open']
    is_doji_second = abs(second_candle['Close'] - second_candle['Open']) < (second_candle['High'] - second_candle['Low']) * 0.1
    is_bullish_third = third_candle['Close'] > third_candle['Open']
    gap_down = second_candle['High'] < first_candle['Low']
    gap_up = third_candle['Low'] > second_candle['High']
    result = is_bearish_first and is_doji_second and is_bullish_third and gap_down and gap_up
    cache[cache_key] = result
    return result

# Example usage
# Assuming 'data' is a pandas DataFrame with the required columns
# while True:
#     print(is_hammer(data))
#     print(is_shooting_star(data))
#     print(is_bullish_abandoned_baby(data))
#     time.sleep(1)  # Simulate real-time data updates
