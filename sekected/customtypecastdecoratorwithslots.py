import time
import numpy as np
from functools import wraps

def convert_init(func):
    @wraps(func)
    def wrapper(self, exch: str, ltp: str, token: str, lotsize: int, strikeprice: float, ticksize: int, OptionType: str, *args, **kwargs):
        self.exch = exch.encode()
        self.ltp = np.uint32(ltp)
        self.token = np.uint32(token)
        self.lotsize = np.int8(lotsize)
        self.strikeprice = np.float32(strikeprice)
        self.ticksize = np.int8(ticksize)
        self.OptionType = OptionType.encode()
        func(self, exch, ltp, token, lotsize, strikeprice, ticksize, OptionType, *args, **kwargs)
    
    return wrapper

class FinInstOnlyDecorat:
    @convert_init
    def __init__(self, exch: str, ltp: str, token: str, lotsize: int, strikeprice: float, ticksize: int, OptionType: str):
        pass
    
#     def print_values(self):
#         print(f"exch: {self.exch}, ltp: {self.ltp}, token: {self.token}, lotsize: {self.lotsize}, strikeprice: {self.strikeprice}, ticksize: {self.ticksize}, OptionType: {self.OptionType}")

# # # Example usage
# # instrument = FinancialInstrument('NSE', '100', '123456', 10, 1500.0, 5, 'Call')
# # instrument.print_values()

# # # Update values with direct method calls
# # instrument.update_values(ltp='200', lotsize=15, strikeprice=1550.5)
# # instrument.print_values()


# Without using __slots__ and convert_init decorator
class FinInstNoDecoratOrSlots:
    def __init__(self, exch: str, ltp: str, token: str, lotsize: int, strikeprice: float, ticksize: int, OptionType: str):
        self.exch = exch
        self.ltp = ltp
        self.token = token
        self.lotsize = lotsize
        self.strikeprice = strikeprice
        self.ticksize = ticksize
        self.OptionType = OptionType

# With __slots__ and convert_init decorator
class FinInstwithDecoratSlots:
    __slots__ = ['exch', 'ltp', 'token', 'lotsize', 'strikeprice', 'ticksize', 'OptionType']

    @convert_init
    def __init__(self, exch: str, ltp: str, token: str, lotsize: int, strikeprice: float, ticksize: int, OptionType: str):
        pass

# Measure time for creation of FinancialInstrumentNoSlots objects
start_time = time.time()
for i in range(1000):  # Create 1000 objects
    instrument = FinInstOnlyDecorat('NSE', '100', '123456', 10, 1500.0, 5, 'Call')
end_time = time.time()
print(f"Time taken FinInstOnlyDecorat: {end_time - start_time} seconds")

# Measure time for creation of FinancialInstrumentWithSlots objects
start_time = time.time()
for i in range(1000):  # Create 1000 objects
    instrument = FinInstNoDecoratOrSlots('NSE', '100', '123456', 10, 1500.0, 5, 'Call')
end_time = time.time()
print(f"Time taken FinInstNoDecoratOrSlots: {end_time - start_time} seconds")

# Measure time for creation of FinancialInstrumentWithSlots objects
start_time = time.time()
for i in range(1000):  # Create 1000 objects
    instrument = FinInstwithDecoratSlots('NSE', '100', '123456', 10, 1500.0, 5, 'Call')
end_time = time.time()
print(f"Time taken FinInstwithDecoratSlots : {end_time - start_time} seconds")
