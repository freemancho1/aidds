import os
import pickle
import pandas as pd
from datetime import datetime

import aidds.sys.config as cfg
from aidds.sys.utils import Logs, AiddsException


def read_data(fcode=None, **kwargs):
    try:
        ftype, fpath = _get_file_path(fcode)
        if ftype == 'pickle':
            with open(fpath, 'rb') as f:
                return pickle.load(f)
        else:
            _, fext = os.path.splitext(fpath)
            if fext.lower() == '.xlsx':
                return pd.read_excel(fpath, **kwargs)
            if fext.lower() == '.csv':
                return pd.read_csv(fpath, **kwargs)
    except Exception as e:
        raise AiddsException('READ_DATA', fcode, str(e))
        
def save_data(data=None, fcode=None, **kwargs):
    try:
        ftype, fpath = _get_file_path(fcode)
        if ftype == 'pickle':
            with open(fpath, 'wb') as f:
                pickle.dump(data, f)
        else:
            # 데이터프레임 저장 시 인덱스를 저장하지 않음
            if 'index' not in kwargs:
                kwargs['index'] = False
            data.to_csv(fpath, **kwargs) 
    except Exception as e:
        raise AiddsException('SAVE_DATA', fcode, str(e))
        
def get_provide_data():
    logs = Logs('GET_PROVIDE_DATA')
    try:
        data = {}
        for key in cfg.DATA_SETs:
            start_time = datetime.now()
            df = read_data(f'PROVIDE,{key}')
            if key == 'SL':
                df = df.rename(columns={'지지물간거리': '인입선지지물간거리'})
            df.rename(columns=_get_rename_cols(df.columns), inplace=True)
            data[key] = df
            value = f'Size{df.shape}, pTime({datetime.now()-start_time})'
            logs.mid(dcode=key, value=value)
        logs.stop()
        return data
    except Exception as e:
        logs.stop()
        raise AiddsException('GET_PROVIDE_DATA', se_msg=str(e))

def get_merged_data():
    logs = Logs('GET_MERGED_DATA')
    try:
        data = {}
        for key in cfg.DATA_SETs:
            # start_time = datetime.now()
            df = read_data(f'MERGE,BATCH,{key}')
            data[key] = df
            # value = f'크기{df.shape}, 처리시간({datetime.now()-start_time})'
            # logs.mid(dcode=key, value=value)
        logs.stop()
        return data
    except Exception as e:
        logs.stop()
        raise AiddsException('GET_MERGED_DATA', se_msg=str(e))

def _get_file_path(fcode=None):
    fcodes = fcode.split(',')
    ftype = 'pickle' if fcodes[0] == 'DUMP' else 'data'
    fkeys = ''.join([f'["{key}"]' for key in fcodes])
    fname = eval('cfg.FILE_NAMEs'+fkeys)
    plist = [cfg.BASE_PATH, ftype, fname]   # path list
    return ftype, os.path.join(*plist)

# 영문으로 변경할 컬럼을 '한글명':'영문명' 형식의 딕셔너리로 변환
def _get_rename_cols(cols=[]):
    return {
        name: cfg.COLs['RENAME'][name] \
            for name in cfg.COLs['RENAME'] if name in cols
    }


if __name__ == '__main__':
    print(_get_file_path('DUMP,SCALER,N1'))