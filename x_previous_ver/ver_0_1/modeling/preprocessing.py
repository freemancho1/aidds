import aidds.sys.config as cfg
from aidds.sys.utils import Logs, AiddsException
from aidds.module.data_io import get_cleaning_data, save_data
from aidds.module.pp_mod import PreprocessingModule

class Preprocessing:
    def __init__(self):
        self.logs = Logs('PP')
        try:
            # Cleaning Data
            self.cdict = {}
            # Preprocessing Data
            self.pdf = None
            self.pp = PreprocessingModule() 
            self._run()
        except AiddsException as ae:
            raise AiddsException('PP', se_msg=ae)
        finally:
            self.logs.stop()
            
    def _run(self):
        try:
            self.cdict = get_cleaning_data()
            self.pdf = self._cons('CONS')
            for key in cfg.DATA_SETs[1:]:
                self.pdf = self._pp_facilitie_data(key)
            # for key in cfg.DATA_SETs:
            #     self.pdf = eval(f'self._{key.lower()}(key)')
            self._pp_to_scaler()
        except AiddsException as ae:
            raise AiddsException('PP_RUN', se_msg=ae)
        
    def _cons(self, key=None):
        logs = Logs(f'PP_{key}')
        try:
            df = self.cdict[key]
            logs.mid('SOURCE', df.shape)
            
            df = self.pp.cons(df)
            
            office_list = df.OFFICE_CD.unique().tolist()
            # 서비스 전처리에 사용하기 위해 사업소 리스트 저장
            save_data(office_list, fcode='DUMP,OFFICE_LIST')
            
            # 사업소 코드를 이용해 사업소 번호로 변경
            office_idxs = []
            for oname in df.OFFICE_CD:
                office_idxs.append(office_list.index(oname))
            df['OFFICE_NO'] = office_idxs
            df = df.drop(columns=['OFFICE_CD'])
            logs.mid('RESULT', df.shape)        
            
            # 설비 갯 수 계산 
            df = self._calculate(df)
            return df
        except AiddsException as ae:
            raise AiddsException(f'PP_{key}', se_msg=ae)
        except Exception as e:
            raise AiddsException(f'PP_{key}', se_msg=e)
        finally:
            logs.stop()
    
    def _calculate(self, sdf=None):
        logs = Logs('PP_CALCULATE')
        try:
            df = self.pp.calculate(sdf, self.cdict)
            logs.mid('CALCULATE', df.shape)
            return df
        except AiddsException as ae:
            raise AiddsException('PP_CALCULATE', se_msg=ae)
        finally:
            logs.stop()
    
    def _pp_facilitie_data(self, key=None):
        logs = Logs(f'PP_{key}')
        try:
            df = self.cdict[key]
            df = eval(f'self.pp.{key.lower()}(df)')
            # 실시간 처리에서 동일 컬럼을 추가하기 위해 학습에서 나온 컬럼 리스트 저장
            cols = df.columns.tolist()
            save_data(cols, fcode=f'DUMP,{key}_ONE_HOT_COLS')
            logs.mid('ONE_HOT', df.shape)
            
            sum_cols = df.columns.tolist()[1:]
            pdf = self.pp.calculate_sum(df, sum_cols, self.pdf)
            logs.mid('RESULT', pdf.shape)
            return pdf
        except AiddsException as ae:
            raise AiddsException(f'PP_{key}', se_msg=ae)
        except Exception as e:
            raise AiddsException(f'PP_{key}', se_msg=e)
        finally:
            logs.stop()
            
    def _pp_to_scaler(self):
        # 최종 완료시점에서 NaN값을 0으로 처리
        # 온라인 작업 시 인입선이 없거나 전주가 없는 작업 등에서 NaN가 올 수 있음
        self.pdf.fillna(0, inplace=True)
        # 모델링 시점과 서비스 시점의 데이터프레임 컬럼 순서를 동일하게 하기 위해
        # 모델링 시점의 컬럼 순서를 저장해 서비스 시점에서 컬럼 순서를 재배치
        # One-Hot Encoding시점에 데이터 컬럼의 순서가 변경될 수 있음.
        save_data(self.pdf.columns, fcode='DUMP,LAST_PP_COLS')
        # 전처리 데이터 저장
        save_data(self.pdf, fcode='PP_LAST')
    