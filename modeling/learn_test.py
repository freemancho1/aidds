import aidds.sys.config as cfg
from aidds.sys.utils.logs import ModelingLogs as Logs
from aidds.sys.utils.data_io import save_data, get_scaling_data, read_data
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
                id: read_data(file_code=f'pickle.models.{id}.best') \
                    for id in cfg.type.pc.ids
            }
            print(f'----- self._best:\n{self._best}')
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

            for pid in cfg.type.pc.ids:
                self._ml_fit_and_evals(pid=pid)

        except Exception as e:
            raise AiddsException(e)
        
    def _ml_fit_and_evals(self, pid=None):
        """ 각 모델과 전주 갯 수에 따라 모델을 학습하고 평가하는 함수
            * 작업결과는 _history와 _best에 저장됨

        Args:
            mid (str, required): 모델 id. Defaults to None.
            pid (str, required): 전주 갯 수 id. Defaults to None.
        """
        try:
            model = self._best[pid]
            # 전주 갯 수별 데이터 불러오기
            # did=data id로 data는 train_x, train_y와 같은 모델링 ds id를 말함
            ddict = {did: self._sdict[did][pid] for did in cfg.type.mds.ids}
            
            # 모델 학습
            modeling_cols = ddict['train_x'].columns.tolist()[1:]
            train_y = ddict[cfg.type.mds.train_y].to_numpy().reshape(-1)
            # 평가를 위해 테스트 데이터 예측
            pred_y = model.predict(ddict[cfg.type.mds.test_x][modeling_cols])
            test_y = ddict[cfg.type.mds.test_y].to_numpy()
            evals, message = \
                regression_evals(y=test_y, p=pred_y, verbose=1)
            # 학습결과 출력
            value = f'Data[{pid.upper()}] - {message}'
            self._logs.mid(code='result', value=value)

        except Exception as e:
            raise AiddsException(e)
        
    def _save_best_model(self):
        """ 전주 갯 수별 최고 모델과 전체 모델의 학습결과 저장 """
        try:
            # 전주 갯 수별 최고 모델 저장
            for pid in cfg.type.pc.ids:
                save_data(
                    data=self._best[pid]['model'],
                    file_code=f'pickle.models.{pid}.best'
                )
            # 전체 모델의 학습결과 저장
            save_data(data=self._history, file_code='pickle.modeling_history')
        except Exception as e:
            raise AiddsException(e)
