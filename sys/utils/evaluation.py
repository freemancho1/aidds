import numpy as np

from sklearn.metrics import mean_absolute_error as mae
from sklearn.metrics import mean_squared_error as mse
from sklearn.metrics import mean_absolute_percentage_error as mape
from sklearn.metrics import r2_score

from aidds.sys.utils.exception import AppException


def regression_evals(y, p, verbose=1) -> list:
    try:
        y = np.round(y, decimals=5)
        p = np.round(p, decimals=5)
        
        _mae = mae(y, p)
        _mse = mse(y, p)
        _rmse = np.sqrt(_mse)
        _mape = mape(y, p)
        _r2score = r2_score(y, p)
        
        if verbose == 1:
            message = f'r2score: {_r2score:.6f}, mape: {_mape:.6f}'
        elif verbose == 2:
            message = f'r2score: {_r2score:.6f}, mape: {_mape:.6f}\n' \
                      f'mae: {_mae:.6f}, mse: {_mse:.6f}, rmse: {_rmse:.6f}'
        else:
            message = ''
        
        return [_mape, _r2score, _mae, _mse, _rmse], message
    except Exception as e:
        raise AppException(e)
    
def calculate_mape(y, p):
    return abs((y-p)/y) * 100