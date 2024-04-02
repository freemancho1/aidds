import aidds.sys.config as cfg
from aidds.sys.utils.logs import ModelingLogs as Logs
from aidds.sys.utils.exception import AiddsException
from aidds.sys.utils.data_io import get_cleaning_data, save_data
from aidds.modeling.pp_module import PreprocessingModule as PPM


class Preprocessing:
    def __init__(self):
        try:
            self._logs = Logs('PP')
            self._cd_dict = {}      # Cleaning DataFrame Dictionary
            self._ppm = PPM()       # Preprocessing Moduel
            self.pdf = None         # Preprocessing DataFrame
            self._run()
        except Exception as e:
            raise AiddsException(e)
        finally:
            if hasattr(self, '_logs'): self._logs.stop()
            
    def _run(self):
        try:
            self._cd_dict = get_cleaning_data()
            self.pdf = self._cons('CONS')
            for key in cfg.DATA_SETs[1:]:
                self._pp_facilities_data(key=key)
            self._completion_of_pp()
        except Exception as e:
            raise AiddsException(e)
        
    def _cons(self, key=None):
        logs = Logs(f'PP_{key}')
        try:
            df = self._cd_dict[key]
            logs.mid('SOURCE', df.shape)
            
            # 전처리 모듈을 이용해 공사비 정보 전처리
            df = self._ppm.cons(df)
            
            # 서비스 시 전처리에 사용하기 위해 사업소 코드 리스트 생성(저장)
            office_cds = df.OFFICE_CD.unique().tolist()
            save_data(office_cds, file_code='DUMP,PP,OFFICE_CDS')
            
            # 사업소 코드들을 이용해 사업소 번호 생성
            office_idxs = [
                office_cds.index(cd) for cd in df.OFFICE_CD
            ]
            df['OFFICE_NO'] = office_idxs
            df = df.drop(columns=['OFFICE_CD'])
            logs.mid('RESULT', df.shape)
            
            # 설비 갯 수 계산
            df = self._ppm.calculate(df, self._cd_dict)
            logs.mid('CALCULATE', df.shape)
            return df
        except (AiddsException, Exception) as e:
            raise AiddsException(e)
        finally:
            logs.stop()
            
    def _pp_facilities_data(self, key=None):
        logs = Logs(f'PP_{key}')
        try:
            df = self._cd_dict[key]
            # 전처리 모듈을 이용해 전주/전선/인입선 정보 전처리
            df = eval(f'self._ppm.{key.lower()}(df)')
            
            # 실시간 처리에서 동일한 컬럼을 추가하기 위해 학습에서 나온
            # 컬럼 리스트를 저장
            cols = df.columns.tolist()
            save_data(cols, file_code=f'DUMP,PP,{key}_ONE_HOT_COLS')
            logs.mid('ONE_HOT', df.shape)
            
            # 설비(전주/전선/인입선)별 합산정보 생성 및
            # 모델링 데이터프레임에 추가
            sum_cols = df.columns.tolist()[1:]
            self.pdf = self._ppm.calculate_sum(df, sum_cols, self.pdf)
            logs.mid('RESULT', self.pdf.shape)
        except Exception as e:
            raise AiddsException(e)
        finally:
            logs.stop()
            
    def _completion_of_pp(self):
        try:
            # 최종 완료시점에서 NaN값을 0으로 처리
            # 온라인 작업 시 인입선이 없거나 전주가 없는 작업 등에서 NaN가 올 수 있음
            self.pdf.fillna(0, inplace=True)
            # 모델링 시점과 서비스 시점의 데이터프레임 컬럼 순서를 동일하게 하기 위해
            # 모델링 시점의 컬럼 순서를 저장해 서비스 시점에서 컬럼 순서를 재배치
            # One-Hot Encoding시점에 데이터 컬럼의 순서가 변경될 수 있음.
            save_data(
                self.pdf.columns, file_code='DUMP,PP,LAST_PP_COLS')
            # 전처리 데이터 저장
            save_data(self.pdf, file_code='PP_LAST')
        except (AiddsException, Exception) as e:
            raise AiddsException(e)
            