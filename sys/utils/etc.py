import numpy as np


def convert_to_builtin_int(obj):
    # If object type np.int64, converted to a Python int
    return int(obj) if isinstance(obj, np.int64) else obj

def convert_to_builtin_float(obj):
    # If object type np.float64, converted to a Python float
    return float(obj) if isinstance(obj, np.float64) else obj

