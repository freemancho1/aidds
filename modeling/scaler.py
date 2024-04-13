import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

import aidds.sys.config as cfg
from aidds.sys.utils.exception import AiddsException
from aidds.sys.utils.logs import ModelingLogs as Logs
from aidds.sys.utils.data_io import save_data, read_data


class Scaling:
    """ 전처리 데이터 스케일링 클래스
    
    Args:
        preprocessing_df (pd.DataFrame): 최종 전처리 데이터프레임
        
    Attributes:
        _ppdf (pd.DataFrame): 스케일링에 사용될 최종 전처리 데이터프레임
        _data         (dict): train_Xy, test_Xy로 분할된 데이터(스케일링 전)
        sdata         (dict): train_Xy, test_Xy로 분할된 데이터(스케일링 후)
    """
    def __init__(self, preprocessing_df=None, is_best=False):
        try:
            self._logs = Logs(code='modeling.scaling')
            self._ppdf = preprocessing_df
            self._data = {}
            self._is_best = is_best
            self.sdata = {}
            self._run()
        except Exception as e:
            raise AiddsException(e)
        finally:
            if hasattr(self, '_logs'):
                self._logs.stop()
                
    def _run(self):
        try:
            # 전처리 데이터를 제공 받지 못한 경우 읽어옴
            if self._is_best:
                self._ppdf = \
                    read_data(file_code='data.pp.best', dtype={'acc_no': str})
            elif self._ppdf is None:
                self._ppdf = \
                    read_data(file_code='data.pp.last', dtype={'acc_no': str})
            # self._data의 데이터 저장 딕셔너리 추가
            # self._data['x']={}, 'y'={}, 'train_x'={}.... 생성
            self._data = {id: {} for id in ['x', 'y'] + cfg.type.mds.ids}
            self.sdata = {id: {} for id in cfg.type.mds.ids}
            # 전체 데이터를 속성과 타겟(예측목표)로 분리
            self._split_xy()
            # 전주 갯 수로 데이터를 분리 후 스케일링
            for id in cfg.type.pc.ids:
                self._scaling(id=id)
            # 데이터 저장
            self._save_data()
        except Exception as e:
            raise AiddsException(e)
                
    def _split_xy(self):
        """ 전처리 데이터에서 목표컬럼과 모델링 컬럼을 분리 """
        try:
            target_col = cfg.col.target
            training_cols = self._ppdf.columns[2:].tolist()
            # 모델링 컬럼정보 저장(서비스에서 사용)
            save_data(training_cols, file_code='pickle.modeling_cols')
            
            # x, y 값 분리
            self._data['x']['all'] = self._ppdf[training_cols].copy()
            self._data['y']['all'] = self._ppdf[target_col].copy()
            self._logs.mid(code='source_x', value=self._data['x']['all'].shape)
        except Exception as e:
            raise AiddsException(e)
        
    def _scaling(self, id=None):
        """ 전주 갯 수로 데이터 분리 후 스케일링 """
        try:
            # 전주 갯 수로 데이터 분할
            if id == cfg.type.pc.all:
                x = self._data['x']['all']
                y = self._data['y']['all']
            else:
                condition = self._data['x']['all'][cfg.col.pc] != 1 \
                    if id == cfg.type.pc.n1 \
                        else self._data['x']['all'][cfg.col.pc] == 1
                x = self._data['x']['all'][condition]
                y = self._data['y']['all'][condition]
                self._data['x'][id] = x
                self._data['y'][id] = y
                
            # 훈련/시험용 데이터로 분할
            train_x, test_x, train_y, test_y = \
                train_test_split(x, y, test_size=0.25)
            value = f'pc_type[{id}] - total{x.shape}, ' \
                    f'train{train_x.shape}, test{test_x.shape}'
            self._logs.mid(code='type_pc', value=value)
            
            # 스케일 전 데이터 저장
            for id2 in cfg.type.mds.ids:
                #             id2        id2     eval(id2)
                # self._data['train_x']['all'] = train_x
                self._data[id2][id] = eval(id2)
                
            # 스케일링
            cols = train_x.columns.tolist()
            scaler = StandardScaler()
            train_x = pd.DataFrame(scaler.fit_transform(train_x), columns=cols)
            test_x = pd.DataFrame(scaler.transform(test_x), columns=cols)
            
            # 스케일 데이터 저장
            for id2 in cfg.type.mds.ids:
                self.sdata[id2][id] = eval(id2)
                
            # 스케일러 저장
            save_data(data=scaler, file_code=f'pickle.scaler.{id}')
        except Exception as e:
            raise AiddsException(e)
                
    def _save_data(self):
        """ 스케일링 전('x','y' 포함)/후 데이터 저장 """
        try:
            for mds_id in cfg.type.mds.ids + ['x', 'y']:
                for pc_id in cfg.type.pc.ids:
                    save_data(
                        data=self._data[mds_id][pc_id],
                        file_code=f'data.split.{mds_id}.{pc_id}'
                    )
                    # 원본 데이터 ['x', 'y']는 스케일링 하지 않음
                    if mds_id in ['x', 'y']:
                        continue
                    save_data(
                        data=self.sdata[mds_id][pc_id],
                        file_code=f'data.scaling.{mds_id}.{pc_id}'
                    )
        except Exception as e:
            raise AiddsException(e)
                