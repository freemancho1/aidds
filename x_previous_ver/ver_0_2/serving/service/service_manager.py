from aidds_buy.sys.utils.logs import service_logs as logs
from aidds_buy.serving.service.samples import Samples
from aidds_buy.serving.service.predict import Predict


class ServiceManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ServiceManager, cls).__new__(cls)
            cls._instance._services = {}
            cls._instance._init_services()
            logs(mcode='SERVICE_MGR')
        return cls._instance
    
    def _init_services(cls):
        # 이곳에 추가하고자 하는 서비스를 추가하고 아래 get()함수를 추가하면
        # 웹에서 다양한 서비스를 싱글톤 방식으로 실행할 수 있음
        cls._instance._services['samples'] = Samples()
        cls._instance._services['predict'] = Predict()
        
    @classmethod
    def get_instance(cls):
        return cls._instance
    
    @classmethod
    def _get_service(cls, service_name=None):
        return cls._instance._services.get(service_name)
    
    # 이 아래 서비스 요청 함수를 실행하면 됨
    
    @classmethod
    def samples(cls):
        return cls._get_service(service_name='samples')
    
    @classmethod
    def predict(cls):
        return cls._get_service(service_name='predict')
        
    
            