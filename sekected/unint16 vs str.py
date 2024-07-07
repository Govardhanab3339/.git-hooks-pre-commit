import pandas as pd
import numpy as np
import sys

# Example data
uint16_data = np.random.randint(0, 65536, size=100000, dtype=np.uint16)
str_data = [str(x) for x in uint16_data]

# Create DataFrames
df_uint16 = pd.DataFrame({'numbers': uint16_data})
df_str = pd.DataFrame({'numbers': str_data})

# Memory usage of the DataFrames
uint16_memory_usage = df_uint16.memory_usage(deep=True).sum()
str_memory_usage = df_str.memory_usage(deep=True).sum()

print(f"Memory usage of DataFrame with uint16: {uint16_memory_usage} bytes")
print(f"Memory usage of DataFrame with str: {str_memory_usage} bytes")
