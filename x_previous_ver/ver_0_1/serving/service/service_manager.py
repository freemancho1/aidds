from aidds_buy.sys.utils import ServiceLogs as Logs
from aidds_buy.serving.service.samples import Samples
from aidds_buy.serving.service.predict import Predict


class ServiceManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ServiceManager, cls).__new__(cls)
            cls._instance._services = {}
            cls._instance._init_services()
            Logs(code='SERVICE_MGR')
        return cls._instance
        
    def _init_services(cls):
        cls._instance._services['samples'] = Samples()
        cls._instance._services['predict'] = Predict()
        cls._instance._services['logs'] = Logs(code='ROUTE')
    
    # @classmethod
    # def get_instance(cls):
    #     return cls._instance
    
    @classmethod
    def _get_service(cls, service_name):
        return cls._instance._services.get(service_name)
    
    @classmethod
    def samples(cls):
        return cls._get_service(service_name='samples')
        
    @classmethod
    def predict(cls):
        return cls._get_service(service_name='predict')
    
    @classmethod
    def logs(cls):
        return cls._get_service(service_name='logs')