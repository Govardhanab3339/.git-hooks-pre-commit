import numpy as np

# Function to print the range of values for a given NumPy float type
def print_float_range(dtype):
    info = np.finfo(dtype)
    print(f"Range for {dtype}: {info.min} to {info.max}")
    print(f"Epsilon for {dtype}: {info.eps}")
    print(f"Smallest positive for {dtype}: {info.tiny}")

# Float types in NumPy
float_types = [np.float16, np.float32, np.float64]

# Print the range for each float type
for dtype in float_types:
    print_float_range(dtype)
