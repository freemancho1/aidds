import os
import pickle
import pandas as pd

from typing import Union
from datetime import datetime
from joblib import dump, load

from aidds.sys import config as cfg
from aidds.sys import messages as msg
from aidds.sys.utils import modeling_logs as logs
from aidds.sys.utils import app_exception


# 'Union' means returning one of the data types in the declared variable
def read_data(code=None, **kwargs) -> Union[pd.DataFrame, bytes]:
    # Read excel, csv, pickle and joblib(model)
    try:
        file_type, file_path, file_ext = _get_file_path(code=code)
        if file_type == cfg.file.type.pickle:
            with open(file_path, 'rb') as file:
                return pickle.load(file)
        elif file_type == cfg.file.type.model:
            return load(file_path)
        else:
            assert file_ext.lower() in [cfg.file.ext.excel, cfg.file.ext.csv], \
                f'{msg.exception.sys.unknown_file_ext} {file_ext}'
            if file_ext.lower() == cfg.file.ext.excel:
                return pd.read_excel(file_path, **kwargs)
            else:
            # if file_ext.lower() == cfg.file.ext.csv:
                return pd.read_csv(file_path, **kwargs)
            # raise app_exception(
            #     f'{msg.exception.sys.unknown_file_ext} {file_ext}'
            # )
    except Exception as e:
        raise app_exception(e)
    
def save_data(data=None, code=None, **kwargs) -> None:
    # Save csv, pickle and joblib(model)
    try:
        file_type, file_path, file_ext = _get_file_path(code=code)
        if file_type == cfg.file.type.pickle:
            with open(file_path, 'wb') as file:
                pickle.dump(data, file)
        elif file_type == cfg.file.type.model:
            dump(data, file_path)
        else:
            assert file_ext.lower() in [cfg.file.ext.excel, cfg.file.ext.csv], \
                f'{msg.exception.sys.unknown_file_ext} {file_ext}'
            # When saving a DataFrame, do not include the index.
            if cfg.sys.utils.data_io.index not in kwargs:
                kwargs[cfg.sys.utils.data_io.index] = False
            if file_ext == cfg.file.ext.excel:
                data.to_excel(file_path, **kwargs)
            else:
                data.to_csv(file_path, **kwargs)
    except Exception as e:
        raise app_exception(e)
    
def get_provide_data() -> dict[str, pd.DataFrame]:
    _logs = logs(code='get_provide_data') 
    try:
        data_dict = {}
        for pkey in cfg.type.pds:
            start_time = datetime.now()
            # Read the provided Excel file
            df = read_data(code=f'data.provide.{pkey}')
            # Change the Korean column names use for training to English
            df.rename(columns=_get_rename_cols(df.columns), inplace=True)
            data_dict[pkey] = df
            value = f'size{df.shape}, ' \
                    f'processing time {datetime.now()-start_time}'
            _logs.mid(code=pkey, value=value)
        return data_dict
    except Exception as e:
        raise app_exception(e)
    finally:
        _logs.stop()
        
def get_cleaning_data() -> dict[str, pd.DataFrame]:
    try:
        return {
            pkey: read_data(code=f'data.cleaning.{pkey}') \
                for pkey in cfg.type.pds
        }
    except Exception as e:
        raise app_exception(e)
    
def get_scaling_data() -> dict[str, any]:
    try:
        sd_dict = {
            tkey: read_data(code=f'data.scaling.{tkey}') \
                for tkey in ['x', 'y'] + cfg.type.tds
        }
        sd_dict[cfg.modeling.cols] = read_data(code='pickle.modeling_cols')
        return sd_dict
    except Exception as e:
        raise app_exception(e)
    
def get_service_pickle() -> tuple[dict[str, bytes], bytes, bytes]:
    try:
        pkl = {
            pkey: read_data(code=f'pickle.{pkey}') \
                for pkey in list(cfg.file.name.pickle.keys())[:-1]
        }
        scaler = read_data(code='pickle.scaler')
        models = read_data(code=f'model.best')
        return pkl, scaler, models
    except Exception as e:
        raise app_exception(e)

def _get_file_path(code=None) -> tuple[str, str, str]:
    try:
        # Find file name and ext
        file_name = eval(f'cfg.file.name.{code}')
        _, file_ext = os.path.splitext(file_name)
        # Get file type
        if file_ext == cfg.file.ext.pickle:
            file_type = cfg.file.type.pickle
        elif file_ext == cfg.file.ext.model:
            file_type = cfg.file.type.model
        else:
            file_type = cfg.file.type.data
        # Get file path list
        file_paths = [cfg.file.base_path, file_type, file_name]
        
        # file_type, file_path, file_ext
        return file_type, os.path.join(*file_paths), file_ext
    except Exception as e:
        raise app_exception(e)
    
def _get_rename_cols(cols=None) -> dict[str, str]:
    try:
        # {'공사번호': 'acc_no', ...}
        return {
            k_name: eval(f'cfg.cols.rename.{k_name}') \
                for k_name in cfg.cols.rename if k_name in cols
        }
    except Exception as e:
        raise app_exception(e)