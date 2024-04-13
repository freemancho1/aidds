from aidds.sys.utils.logs import service_logs as logs
from aidds.serving.service.samples import Samples


class ServiceManager:
    """ 웹 서비스를 위한 RESTAPI 서비스 메니저 싱글톤 클래스 """
    _instance = None
        
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ServiceManager, cls).__new__(cls)
            # 서비스 등록용 딕셔너리
            cls._instance._services = {}
            # 서비스 초기화(웹 서비스에 초기 로딩) 함수
            cls._instance._init_services()
            logs(code='manager')
        return cls._instance
    
    def _init_services(cls):
        # 이곳에 추가할 서비스 등록
        cls._instance._services['samples'] = Samples()
        
    # 이곳에 추가할 서비스 요청함수 생성
    
    @classmethod
    def samples(cls):
        return cls._get_service(service_name='samples')
    
    
    # 자체적으로 사용하는 클래스함수
        
    @classmethod
    def get_instance(cls):
        return cls._instance
    
    @classmethod
    def _get_service(cls, service_name=None):
        return cls._instance._services.get(service_name)
        