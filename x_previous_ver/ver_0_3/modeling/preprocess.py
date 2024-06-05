import aidds_buy.sys.config as cfg
from aidds_buy.sys.utils.logs import ModelingLogs as Logs
from aidds_buy.sys.utils.exception import AiddsException
from aidds_buy.sys.utils.data_io import get_cleaning_data, save_data
from aidds_buy.modeling.pp_module import PreprocessingModule as ppm


class Preprocessing:
    """ 모델링 부분 전처리 메인 클래스 
    
    Args:
        cd_dict      (dict): 크리닝된 공사비+설비 데이터
        
    Attributes:
        _cd_dict     (dict): 전처리에 사용할 크리닝 데이터
        _ppm        (class): 모델링과 서비스에서 공통으로 사용할 전처리 모듈 클래스
        ppdf (pd.DataFrame): 최종 전처리 된 데이터프레임(스케일링에 사용됨)
    """
    
    def __init__(self, cd_dict=None):
        try:
            self._logs = Logs(code='modeling.pp')
            self._cd_dict = cd_dict
            self._ppm = ppm()
            self.ppdf = None
            self._run()
        except Exception as e:
            raise AiddsException(e)
        finally:
            if hasattr(self, '_logs'): self._logs.stop()
            
    def _run(self):
        try:
            # 입력된 클리닝 데이터가 없으면 읽어오기
            if self._cd_dict is None:
                self._cd_dict = get_cleaning_data()
            # 공사비 데이터 전처리
            self._cons()
            # 설비(전주/전선/인입선) 데이터 전처리
            for id in cfg.type.pds.ids[1:]:
                self._facilities_data(id=id)
            # 전처리 종료: 최종 NaN처리, 컬럼정보 저장, 데이터 저장
            self._completion_of_pp()
        except Exception as e:
            raise AiddsException(e)
        
    def _cons(self):
        """ 모델링 부분 공사비 전처리 함수 """
        logs = Logs(code='modeling.pp.cons')
        try:
            df = self._cd_dict[cfg.type.pds.cons]
            logs.mid(code='source', value=df.shape)
            # 공통 모듈을 이용해 공사비 정보 전처리
            df = self._ppm.cons(cons_df=df)
            
            # 서비스 전처리용 사업소 코드 리스트 생성 및 저장
            office_codes = df.office_cd.unique().tolist()
            save_data(office_codes, file_code='pickle.pp.office.codes')       
            # 사업소 코드를 이용해 사업소 번호 생성
            office_ids = [office_codes.index(code) for code in df.office_cd]
            df[cfg.col.base.office_id] = office_ids
            df = df.drop(columns=[cfg.col.base.office_cd])
            logs.mid(code='result', value=df.shape)
            
            # 설비 갯 수 계산
            df = self._ppm.calculate(pp_df=df, cd_dict=self._cd_dict)
            logs.mid(code='calculate', value=df.shape)
            
            # 공사비 전처리 데이터 클래스에 저장
            self.ppdf = df
        except Exception as e:
            raise AiddsException(e)
        finally: 
            logs.stop()
            
    def _facilities_data(self, id=None):
        """ 모델링 부분 설비(전주/전선/인입선) 전처리 함수 """
        logs = Logs(code=f'modeling.pp.{id}')
        
        try:
            # 설비데이터 불러오기
            df = self._cd_dict[id]
            # 전처리 모듈을 이용해 설비데이터 전처리
            df = eval(f'self._ppm.{id}({id}_df=df)')
            
            # 실시간 처리에서 동일한 컬럼을 추가하기 위해,
            # 학습에서 나온 컬럼 리스트 저장
            cols = df.columns.tolist()
            save_data(cols, file_code=f'pickle.pp.one_hot_cols.{id}')
            logs.mid(code='one_hot', value=df.shape)
            
            # 설비(전주/전선/인입선)별 합산정보 생성 및
            # 모델링 데이터프레임에 추가
            sum_cols = df.columns.tolist()[1:]
            self.ppdf = self._ppm.summary(df=df, cols=sum_cols, ppdf=self.ppdf)
            logs.mid(code='result', value=self.ppdf.shape)
        except Exception as e:
            raise AiddsException(e)
        finally:
            logs.stop()
        
    def _completion_of_pp(self):
        """ 전처리 종료: 최종 NaN처리, 컬럼정보 저장, 데이터 저장 """
        
        try:
            # 최종완료 시점에 NaN 처리
            self.ppdf = self.ppdf.fillna(0)
            
            # 모델링 시점과 서비스 시점의 데이터프레임 컬럼 정보를 동일하게
            # 처리하기 위해 모델링 시점의 컬럼정보 저장
            # (서비스 시점에 컬럼 재배치, One-Hot등에 의해 컬럼위치 변경 가능성 있음)
            save_data(
                data=self.ppdf.columns.tolist(),
                file_code='pickle.pp.last_cols'
            )
            
            # 전처리 데이터 저장
            save_data(self.ppdf, file_code='data.pp.last')
        except Exception as e:
            raise AiddsException(e)
            