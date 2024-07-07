import numpy as np

# Example of creating arrays with string and character types
str_array = np.array(['a', 'bc', 'def'], dtype='U')  # Unicode string
bytes_array = np.array([b'a', b'bc', b'def'], dtype='S')  # Byte string

# Print information about the string arrays
print(f"String array dtype: {str_array.dtype}, max length: {str_array.dtype.itemsize}")
print(f"Byte string array dtype: {bytes_array.dtype}, max length: {bytes_array.dtype.itemsize}")

# Character type example
char_array = np.array(['a', 'b', 'c'], dtype='c')
print(f"Character array dtype: {char_array.dtype} , max length: {char_array.dtype.itemsize}")
