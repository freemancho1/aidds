import aidds_buy.sys.config as cfg 
from aidds_buy.sys.utils.logs import ModelingLogs as Logs
from aidds_buy.sys.utils.data_io import save_data
from aidds_buy.sys.utils.exception import AiddsException
from aidds_buy.sys.utils.evaluations import regression_evals


class Learning:
    def __init__(self, scaling_data=None):
        try:
            self._logs = Logs('LEARNING')
            self._sdata = scaling_data
            self._best = {
                pc_key: {'MODEL': None, 'SCORE': 0, 'MODEL_KEY': ''} \
                    for pc_key in cfg.PC_TYPEs
            }
            self._history = {}
            self._run()
        except Exception as e:
            raise AiddsException(e)
        finally:
            if hasattr(self, '_logs'): self._logs.stop()
            
    def _run(self):
        try:
            # 모델별 학습
            for md_key in cfg.MODEL_KEYs:
                # 데이터 유형별 학습 = 모델별 데이터 유형별 학습
                for pc_key in cfg.PC_TYPEs:
                    self._ml_fit_and_evals(md_key=md_key, pc_key=pc_key)
            # 데이터 유형별 최고 모델 저장
            self._save_best_model()
        except Exception as e:
            raise AiddsException(e)
        
    def _ml_fit_and_evals(self, md_key=None, pc_key=None):
        try:
            model = cfg.MODELs['ML'][md_key]
            data = {
                dt_key: self._sdata[f'{dt_key}_{pc_key}'] \
                    for dt_key in cfg.DATA_TYPEs
            }
            train_y = data['TRAIN_y'].to_numpy().reshape(-1)
            
            model.fit(data['TRAIN_X'], train_y)
            
            pred_y = model.predict(data['TEST_X'])
            test_y = data['TEST_y'].to_numpy().reshape(-1)
            evals, message = \
                regression_evals(y=test_y, p=pred_y, verbose=1)
            value = f'MODEL[{md_key}], Data[{pc_key}] - {message}'
            self._logs.mid(mcode='RESULT', value=value)
            
            # 데이터 유형별 최고 모델 설별
            if self._best[pc_key]['SCORE'] < evals[2]:
                self._best[pc_key].update({
                    'SCORE': evals[2], 'MODEL': model, 'MODEL_KEY': md_key,
                })
            
            # 학습결과 모델 저장
            save_data(model, file_code=f'DUMP,MODELS,{pc_key},{md_key}')
            # 학습결과 평가내용 클래스에 저장
            self._history[f'{md_key}_{pc_key}'] = evals
        except Exception as e:
            raise AiddsException(e)
        
    def _save_best_model(self):
        try:
            # 데이터 유형별 최고모델 저장
            for pc_key in cfg.PC_TYPEs:
                save_data(
                    data=self._best[pc_key]['MODEL'],
                    file_code=f'DUMP,MODELS,{pc_key},BEST'
                )
            # 전체 모델학습 평가 결과 저장
            save_data(
                data=self._history, 
                file_code='DUMP,MODELING_HISTORY'
            )
        except Exception as e:
            raise AiddsException(e)