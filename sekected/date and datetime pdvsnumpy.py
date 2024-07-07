import pandas as pd
import numpy as np
import time

# Create a large pandas DataFrame with datetime and timedelta columns
n = 1000000
data = {
    'datetime': pd.date_range('2023-01-01', periods=n, freq='min'),
    'timedelta': pd.to_timedelta(np.random.randint(1, 1000, size=n), unit='s')
}

df = pd.DataFrame(data)

# Convert pandas datetime and timedelta columns to NumPy formats
df['datetime_np'] = df['datetime'].values.astype('datetime64[ns]')
df['timedelta_np'] = df['timedelta'].values.astype('timedelta64[ns]')

# Sorting using pandas datetime column
start_time = time.time()
df_sorted_pandas = df.sort_values(by='datetime')
pandas_sort_time = time.time() - start_time
print(f"Time to sort using pandas datetime column: {pandas_sort_time:.6f} seconds")

# Sorting using NumPy datetime column
start_time = time.time()
df_sorted_numpy = df.sort_values(by='datetime_np')
numpy_sort_time = time.time() - start_time
print(f"Time to sort using NumPy datetime column: {numpy_sort_time:.6f} seconds")
