import aidds.sys.config as cfg
from aidds.sys.utils.logs import ModelingLogs as Logs
from aidds.sys.utils.data_io import save_data, get_scaling_data
from aidds.sys.utils.exception import AiddsException
from aidds.sys.utils.evaluation import regression_evals


class Learning:
    """ 9개의 모델을 훈련해 최상의 모델을 저장하는 클래스
    Args:
        scaling_data ({pd.DataFrame}): 스케일링 데이터의 데이터프레임 딕셔너리
    Attributes:
        _sdict ({pd.DataFrame}): 입력받은 스케일링 데이터 데이터프레임 딕셔너리
        _best            (dict): 전주 갯 수별 최고 성능의 모델 정보
                                 (model, score, model_key)
        _history         (dict): 전주 갯 수 및 모델별 성능 지표
    """
    def __init__(self, scaling_data=None):
        try:
            self._logs = Logs(code='learning') 
            self._sdict = scaling_data
            self._best = {
                id: {'model': None, 'score': 0, 'mape': 0, 'model_key': ''} \
                    for id in cfg.type.pc.ids
            }
            self._history = {}
            self._run()
        except Exception as e:
            raise AiddsException(e)
        finally:
            if hasattr(self, '_logs'):
                self._logs.stop()
                
    def _run(self):
        try:
            # 입력받은 데이터가 없으면 읽어오기
            if self._sdict is None:
                self._sdict = get_scaling_data()
            # 모델별 학습
            for mid in cfg.model.ids:
                # 전주 갯 수별 학습 => 모델 및 전주 갯 수별 학습
                for pid in cfg.type.pc.ids:
                    self._history[pid] = {}
                    self._ml_fit_and_evals(mid=mid, pid=pid)
            self._best_model_predict()
            # 데이터 유형별 최고 모델 저장(서비스에서 사용)
            self._save_best_model()
            # 임시 작업(최고 모델로 다시 모델링해서 결과 확인)
            self._best_model_predict()
        except Exception as e:
            raise AiddsException(e)
        
    def _ml_fit_and_evals(self, mid=None, pid=None):
        """ 각 모델과 전주 갯 수에 따라 모델을 학습하고 평가하는 함수
            * 작업결과는 _history와 _best에 저장됨

        Args:
            mid (str, required): 모델 id. Defaults to None.
            pid (str, required): 전주 갯 수 id. Defaults to None.
        """
        try:
            model = eval(f'cfg.model.ml.{mid}')
            # 전주 갯 수별 데이터 불러오기
            # did=data id로 data는 train_x, train_y와 같은 모델링 ds id를 말함
            ddict = {did: self._sdict[did][pid] for did in cfg.type.mds.ids}
            
            # 모델 학습
            train_y = ddict[cfg.type.mds.train_y].to_numpy().reshape(-1)
            model.fit(ddict[cfg.type.mds.train_x], train_y)
            # 평가를 위해 테스트 데이터 예측
            pred_y = model.predict(ddict[cfg.type.mds.test_x])
            test_y = ddict[cfg.type.mds.test_y].to_numpy()
            evals, message = \
                regression_evals(y=test_y, p=pred_y, verbose=1)
            # 학습결과 출력
            # value = f'MODEL[{mid.upper()}], Data[{pid.upper()}] - {message}'
            # self._logs.mid(code='result', value=value)
            
            # 데이터 유형별 최고 모델 선별
            if self._best[pid]['score'] < evals[1]:
                self._best[pid].update({
                    'score': evals[1], 'mape': evals[0], \
                    'model': model, 'model_key': mid
                })
            
            # 재학습(임시코드)
            if mid=='gbr' and pid=='all':
                print(self._best)
                print(ddict['test_x'].loc[0, 'cont_cap'])
                pred_y = model.predict(ddict['test_x'])
                evals, message = \
                regression_evals(y=test_y, p=pred_y, verbose=1)
                value = f'[모델 그대로 사용] - {message}'
                self._logs.mid(code='result', value=value)

                model = self._best['all']['model']
                pred_y = model.predict(ddict['test_x'])
                evals, message = \
                regression_evals(y=test_y, p=pred_y, verbose=1)
                value = f'[읽어들인 모델 사용] - {message}'
                self._logs.mid(code='result', value=value)
                
                self._best_model_predict()

            
            
            # 학습결과 모델 저장
            save_data(data=model, file_code=f'pickle.models.{pid}.{mid}')
            # 모델 평가 결과 클래스에 저장
            self._history[pid][mid] = evals
        except Exception as e:
            raise AiddsException(e)
        
    def _save_best_model(self):
        """ 전주 갯 수별 최고 모델과 전체 모델의 학습결과 저장 """
        try:
            self._best_model_predict()
            # 전주 갯 수별 최고 모델 저장
            for pid in cfg.type.pc.ids:
                save_data(
                    data=self._best[pid]['model'],
                    file_code=f'pickle.models.{pid}.best'
                )
            self._best_model_predict()
            # 전체 모델의 학습결과 저장
            save_data(data=self._history, file_code='pickle.modeling_history')
        except Exception as e:
            raise AiddsException(e)
        
    def _best_model_predict(self):
        try:
            # 전주 갯 수별 데이터 불러오기
            # did=data id로 data는 train_x, train_y와 같은 모델링 ds id를 말함
            # ddict = {did: self._sdict[did][pid] for did in cfg.type.mds.ids}
            test_x = self._sdict['test_x']['all']
            print(test_x.loc[0, 'cont_cap'])
            test_y = self._sdict['test_y']['all'].to_numpy()
            
            model = self._best['all']['model']
            print(self._best)
            pred_y = model.predict(test_x)
            evals, message = \
                regression_evals(y=test_y, p=pred_y, verbose=1)
            value = f'[1111111111] - {message}'
            self._logs.mid(code='result', value=value)
        except Exception as e:
            raise AiddsException(e)
        
