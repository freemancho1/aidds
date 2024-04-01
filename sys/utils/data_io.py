import os
import pickle
import pandas as pd
from datetime import datetime 

import aidds.sys.config as cfg 
import aidds.sys.messages as msg
from aidds.sys.utils.logs import ModelingLogs as Logs
from aidds.sys.utils.exception import AiddsException 


def read_data(file_code=None, **kwargs):
    try:
        file_type, file_path = _get_file_path(file_code=file_code)
        if file_type == cfg.FILE_TYPE_PICKLE:
            with open(file_path, 'rb') as file:
                return pickle.load(file)
        else:
            _, file_ext = os.path.splitext(file_path)
            if file_ext.lower() == cfg.FILE_EXT_EXCEL:
                return pd.read_excel(file_path, **kwargs)
            elif file_ext.lower() == cfg.FILE_EXT_CSV:
                return pd.read_csv(file_path, **kwargs)
            else:
                # 이거 테스트 필요
                raise AiddsException(
                    f'{msg.EXCEPIONs["UNKNOWN_FILE_EXT"]} {file_path}')
    except AiddsException as ae: 
        raise AiddsException(ae)
    except Exception as e:
        raise AiddsException(e)
    
def save_data(data=None, file_code=None, **kwargs):
    try:
        file_type, file_path = _get_file_path(file_code=file_code)
        if file_type == cfg.FILE_TYPE_PICKLE:
            with open(file_path, 'wb') as file:
                pickle.dump(data, file)
        else:
            # 데이터프레임 저장 시 인덱스를 저장하지 않음
            if 'index' not in kwargs:
                kwargs['index'] = False
            data.to_csv(file_path, **kwargs)
    except AiddsException as ae: 
        raise AiddsException(ae)
    except Exception as e:
        raise AiddsException(e)
    
def get_provide_data():
    logs = Logs('GET_PROVIDE_DATA')
    try:
        data_dict = {}
        for key in cfg.DATA_SETs:
            start_time = datetime.now()
            df = read_data(f'{PROVIDE,{key}}')
            if key == 'SL':
                df = df.rename(columns={'지지물간거리': '인입선지지물간거리'})
            df.rename(columns=_get_rename_cols(df.columns), inplace=True)
            data_dict[key] = df
            value = f'Size{df.shape}, Processing Time {datetime.now()-start_time}'
            logs.mid(mcode=key, value=value)
        return data_dict
    except AiddsException as ae:
        raise AiddsException(ae)
    except Exception as e:
        raise AiddsException(e)
    finally:
        logs.stop()
        
def get_cleaning_data():
    try:
        return {key: read_data(f'CLEANING,BATCH,{key}') for key in cfg.DATA_SETs}
    except AiddsException as ae:
        raise AiddsException(ae)
    except Exception as e:
        raise AiddsException(e)


def _get_file_path(file_code=None):
    try:
        file_codes = file_code.split(',')
        file_type = cfg.FILE_TYPE_PICKLE \
            if file_codes[0] == 'DUMP' else cfg.FILE_TYPE_DATA
        file_keys = ''.join([f'["{code}"]' for code in file_codes])
        file_name = eval('cfg.FILE_NAMEs'+file_keys)
        paths = [cfg.BASE_PATH, file_type, file_name]
        return file_type, os.path.join(*paths)
    except Exception as e:
        raise AiddsException(e)

def _get_rename_cols(cols=None):
    try:
        return {
            name: cfg.COLs['RENAME'][name] \
                for name in cfg.COLs['RENAME'] if name in cols
        }
    except Exception as e:
        raise AiddsException(e)