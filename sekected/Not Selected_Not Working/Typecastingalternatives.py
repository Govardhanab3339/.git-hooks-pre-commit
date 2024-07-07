class MyClass:
    __slots__ = ['a', 'b', 'c']

    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

# Without __slots__
class WithoutSlots:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

from dataclasses import dataclass

@dataclass
class MyDataClass:
    __slots__ = ['a', 'b', 'c']
    a: int
    b: int
    c: int

# Memory comparison




# Memory comparison
import sys
obj_with_dataclass_slots = MyDataClass(1, 2, 3)

obj_with_slots = MyClass(1, 2, 3)
obj_without_slots = WithoutSlots(1, 2, 3)
print("obj_with_slots " ,sys.getsizeof(obj_with_slots))  # Smaller size
print("obj_without_slots ", sys.getsizeof(obj_without_slots))  # Larger size due to __dict__
print("obj_with_dataclass_slots  ", sys.getsizeof(obj_with_dataclass_slots))  # Smaller size
