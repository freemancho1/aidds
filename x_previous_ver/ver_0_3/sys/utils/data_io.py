import os
import pickle
import pandas as pd
from typing import Tuple
from datetime import datetime

import aidds_buy.sys.config as cfg
import aidds_buy.sys.message as msg
from aidds_buy.sys.utils.logs import ModelingLogs as Logs
from aidds_buy.sys.utils.exception import AiddsException


def read_data(file_code=None, **kwargs):
    try:
        file_type, file_path, file_ext = _get_file_path(file_code)
        if file_type == cfg.file.type.pickle:
            with open(file_path, cfg.sys.pickle.read) as file:
                return pickle.load(file)
        else:
            if file_ext.lower() == cfg.file.ext.excel:
                return pd.read_excel(file_path, **kwargs)
            if file_ext.lower() == cfg.file.ext.csv:
                return pd.read_csv(file_path, **kwargs)
            raise AiddsException(
                f'{msg.exception.sys.unknown_file_ext} {file_ext}')
    except Exception as e:
        raise AiddsException(e) 
    
    
def save_data(data=None, file_code=None, **kwargs):
    try:
        file_type, file_path, file_ext = _get_file_path(file_code)
        if file_type == cfg.file.type.pickle:
            with open(file_path, cfg.sys.pickle.write) as file:
                pickle.dump(data, file)
        else:
            # 데이터프레임 저장시 인덱스를 저장하지 않음
            if cfg.sys.index not in kwargs:
                kwargs[cfg.sys.index] = False
            if file_ext.lower() == cfg.file.ext.excel:
                data.to_excel(file_path, **kwargs)
            elif file_ext.lower() == cfg.file.ext.csv:
                data.to_csv(file_path, **kwargs)
            else:
                raise AiddsException(
                    f'{msg.exception.sys.unknown_file_ext} {file_ext}')
    except Exception as e:
        raise AiddsException(e)
    
    
def get_provide_data():
    logs = Logs(code='modeling.get_provide_data')
    try:
        data_dict = {}
        for id in cfg.type.pds.ids:
            start_time = datetime.now()
            df = read_data(file_code='data.provide.'+id)
            df.rename(columns=_get_rename_cols(df.columns), inplace=True)
            data_dict[id] = df
            value = f'Size{df.shape}, '\
                    f'Processing Time {datetime.now()-start_time}'
            logs.mid(code=id, value=value)
        return data_dict
    except Exception as e:
        raise AiddsException(e)
    finally:
        logs.stop()

def get_cleaning_data() -> dict:
    try:
        return {
            id: read_data(f'data.cleaning.{id}') \
                for id in cfg.type.pds.ids
        }
    except Exception as e:
        raise AiddsException(e)
    
def get_scaling_data() -> dict:
    try:
        return {
            mid: {
                pid: read_data(file_code=f'data.scaling.{mid}.{pid}') \
                    for pid in cfg.type.pc.ids
            } for mid in cfg.type.mds.ids
        }
    except Exception as e:
        raise AiddsException(e)
    
def get_service_pickle():
    pickle_list = []
    
    def get_pickle_list(data_dict=None, parent_key='', sep='.'):
        try:
            for key, value in data_dict.items():
                new_key = f'{parent_key}{sep}{key}' if parent_key else key
                if isinstance(value, dict):
                    # 모델 피클중 best모델만 추출
                    if new_key.startswith('models.'):
                        pickle_list.append(f'{new_key}.best')
                    else:
                        get_pickle_list(data_dict=value, parent_key=new_key)
                else:
                    # 'modeling_history'는 필요없으니 제거
                    if new_key.startswith('modeling_history'):
                        pass
                    else:
                        pickle_list.append(new_key)
                        # 딕셔너리로 가져올 때는
                        # pickle_dict[new_key] = value                        
        except Exception as e:
            raise AiddsException(e)

    try:
        get_pickle_list(cfg.file.name.pickle)
        return {
            id: read_data(file_code=f'pickle.{id}') \
                for id in pickle_list
        }
    except Exception as e:
        raise AiddsException(e)
    
def _get_file_path(file_code=None) -> Tuple[str, str, str]:
    try:
        # 파일명 찾기
        file_name = eval('cfg.file.name.'+file_code)
        # 파일명에서 확장자를 분리해
        _, file_ext = os.path.splitext(file_name)
        # 확장자가 pickle이면 타입을 pickle, 아니면 data로 지정
        file_type = cfg.file.type.pickle \
            if file_ext == cfg.file.ext.pickle \
            else cfg.file.type.data
        file_paths = [cfg.file.base_path, file_type, file_name]
        # 파일타입, 파일경로(이름포함), 파일확장자 리턴
        return file_type, os.path.join(*file_paths), file_ext
    except Exception as e:
        raise AiddsException(e)
    
def _get_rename_cols(cols=None):
    try:
        # {'공사번호': 'acc_no'...} 이렇게 변환됨
        return {
            name: eval(f'cfg.col.rename.{name}') \
                for name in cfg.col.rename if name in cols
        }
    except Exception as e:
        raise AiddsException(e)