import numpy as np

# Function to print the range of values for a given NumPy integer type
def print_int_range(dtype):
    info = np.iinfo(dtype)
    print(f"Range for {dtype}: {info.min} to {info.max}")

# Integer types in NumPy
int_types = [np.int8, np.int16, np.int32, np.int64, np.uint8, np.uint16, np.uint32, np.uint64]

# Print the range for each integer type
for dtype in int_types:
    print_int_range(dtype)
