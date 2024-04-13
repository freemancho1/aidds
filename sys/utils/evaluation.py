import numpy as np

from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_percentage_error
from sklearn.metrics import r2_score

from aidds.sys.utils.exception import AiddsException


def user_mape(y, p):
    try:
        print(f'=== TYPE: y[{type(y)}], p[{type(p)}]')
        print(f'=== SHAPE: y[{y.shape}], p[{p.shape}]')
        max_value = max(np.max(y), 1)
        umape = 0.0  
        data_size = len(y)
        for i in range(data_size):
            (_y, _p) = (max_value, p[i]+max_value) if y[i]<1 else (y[i], p[i])
            umape += abs((_y-_p)/_y)
        umape = umape / data_size
        print(f'=== TYPE & shape: type[{type(umape)}], shape[{umape.shape}]')
        return umape 
    except Exception as e:
        raise AiddsException(e)

def regression_evals(y, p, verbose=1):
    try:
        # Numpy 자체 버그해결을 목적으로 모든 값을 소숫점 5자리에서 반올림
        y = np.round(y, decimals=5)
        p = np.round(p, decimals=5)
        
        mse = mean_squared_error(y, p)
        rmse = np.sqrt(mse)
        mae = mean_absolute_error(y, p)
        r2score = r2_score(y, p)
        mape = mean_absolute_percentage_error(y, p)
        # umape = user_mape(y, p)
        
        message = \
            f'MAPE: {mape:.6f}, ' \
            f'R2SCORE: {r2score:.6f}, \nMAE: {mae:.6f}, MSE: {mse:.6f}, ' \
            f'RMSE: {rmse:.6f}' if verbose == 2 \
        else \
            f'MAPE: {mape:.6f}, ' \
            f'R2SCORE: {r2score:.6f}' if verbose == 1 \
        else ''
        return [mape, r2score, mae, mse, rmse], message
    except Exception as e:
        raise AiddsException(e)