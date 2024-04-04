import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

import aidds.sys.config as cfg
from aidds.sys.utils.exception import AiddsException
from aidds.sys.utils.logs import ModelingLogs as Logs
from aidds.sys.utils.data_io import read_data, save_data


class Scaling:
    def __init__(self, preprocessing_data=None):
        try: 
            self._logs = Logs('SCALING')
            self._pdf = preprocessing_data
            self._data = {}     # 분할된 스케일링 전 데이터
            self.sdata = {}     # 분할된 스케일링 데이터
            self._run()
        except Exception as e:
            raise AiddsException(e)
        finally: 
            if hasattr(self, '_logs'): self._logs.stop()
            
    def _run(self):
        try:
            # 전체 데이터를 속성과 타겟(예측목표)로 분리
            self._split_Xy()
            for pc_key in cfg.PC_TYPEs:
                self._scaling(pc_key=pc_key)
        except Exception as e:
            raise AiddsException(e)
        
    def _split_Xy(self):
        try:
            # TARGET 컬럼 지정
            target_col = cfg.COLs['TARGET']
            # 학습컬럼 지정
            training_cols = self._pdf.columns[2:].tolist()
            #모델링 컬럼 정보 저장
            save_data(training_cols, file_code='DUMP,MODELING_COLS')
            
            # X, y값 분리
            self._data['X_ALL'] = self._pdf[training_cols].copy()
            self._data['y_ALL'] = self._pdf[target_col].copy()
            self._logs.mid('SOURCE_X', self._data['X_ALL'].shape)
            
            # 학습데이터 저장
            save_data(self._data['X_ALL'], file_code='SCALING,X,ALL')
            save_data(self._data['y_ALL'], file_code='SCALING,y,ALL')
        except Exception as e:
            raise AiddException(e)
        
    def _scaling(self, pc_key=None):
        try:
            if pc_key == 'ALL':
                X = self._data['X_ALL']
                y = self._data['y_ALL']
            else:
                condition = self._data['X_ALL'].POLE_CNT == 1 \
                    if pc_key == '1' else self._data['X_ALL'].POLE_CNT != 1
                X = self._data['X_ALL'][condition]
                y = self._data['y_All'][condition]
                self._logs.mid('PC_TYPE_X', f'[{pc_key}] attr data size {X.shape}')
                # 저장
                self._data[f'X_{pc_key}'] = X
                self._data[f'y_{pc_key}'] = y
                save_data(X, file_code=f'SCALING,X,{pc_key}')
                save_data(y, file_code=f'SCALING,y,{pc_key}')

            # 분할
            train_X, test_X, train_y, test_y = \
                train_test_split(X, y, test_size=0.2)
            message = f'PC_TYPE[{pc_key}] Total{X.shape}, ' \
                      f'Train{train_X.shape}, Test{test_X.shape}'
            self._logs.mid('PC_TYPE_TT', value=message)
            
            # 스케일 전 데이터 저장
            self._data[f'TRAIN_X_{pc_key}'] = train_X
            self._data[f'TRAIN_y_{pc_key}'] = train_y
            self._data[f'TEST_X_{pc_key}'] = test_X
            self._data[f'TEST_y_{pc_key}'] = test_y
            
            # 스케일링
            cols = train_X.columns.tolist()
            scaler = StandardScaler()
            train_SX = scaler.fit_transform(train_X)
            test_SX = scaler.transform(test_X)
            train_SX_df = pd.DataFrame(train_SX, columns=cols)
            test_SX_df = pd.DataFrame(test_SX, columns=cols)
            
            # 클래스에 저장
            self.sdata[f'TRAIN_X_{pc_key}'] = train_SX_df
            self.sdata[f'TRAIN_y_{pc_key}'] = train_y
            self.sdata[f'TEST_X_{pc_key}'] = test_SX_df
            self.sdata[f'TEST_y_{pc_key}'] = test_y
            
            # 스케일러 저장
            save_data(scaler, file_code=f'DUMP,SCALER,{pc_key}')
        except Exception as e:
            raise AiddsException(e)