import numpy as np


def convert_to_builtin_int(obj):
    """ 입력받은 객체가 np.int64형이면 파이썬 int형으로 변환함 """
    return int(obj) if isinstance(obj, np.int64) else obj