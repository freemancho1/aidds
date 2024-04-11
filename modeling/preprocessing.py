import aidds.sys.config as cfg
import aidds.sys.message as msg
from aidds.sys.utils.log import ModelingLogs as Logs
from aidds.sys.utils.exception import AiddsException
from aidds.sys.utils.data_io import get_cleaning_data, save_data
from aidds.modeling.pp_module import PreprocessingModule as ppm


class Preprocessing:
    """ 모델링 부분 전처리 메인 클래스 """
    
    def __init__(self, cd_dict=None):
        try:
            self._logs = Logs(msg.log.modeling.pp.main)
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
            if self._cd_dict is None:
                self._cd_dict = get_cleaning_data()
            self.ppdf = self._cons()
            
        except Exception as e:
            raise AiddsException(e)
        
    def _cons(self) -> pd.DataFrame:
        """ 모델링 부분 공사비 전처리 함수 """
        logs = Logs(msg.log.modeling.pp.cons.main)
        try:
            df = self._cd_dict[cfg.type.pds.cons]
            logs.mid(
                message=msg.log.modeling.pp.cons.source,
                value=df.shape
            )
            # 공통 모듈을 이용해 공사비 정보 전처리
            df = self._ppm.cons(cons_df=df)
            
            # 서비스 전처리용 사업소 코드 리스트 생성 및 저장
            office_codes = df.office_cd.unique().tolist()
            save_data(office_codes, file_code='pickle.pp.office.codes')
            ###############
            ############### 여기서부터 하는데,
            ############### 사업소코드 한번 확인하고 변경 처리 추가여부 결정
            ############### 아직 사업소 명 데이터만 가지고 있으니....
            ###############
        except Exception as e:
            raise AiddsException(e)
        finally: 
            logs.stop()
            
            
            