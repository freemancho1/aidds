from aidds import service_logs as logs

# Singleton service 
from aidds.serving import samples_service
from aidds.serving import predict_service


class ServiceManager:
    """ REST API singleton service manager for web service """
    
    def _init_services(cls):
        # Register services to add here
        cls._instance._services['samples'] = samples_service()
        cls._instance._services['predict'] = predict_service()
        
    # Define the service request function to be add here
    
    @classmethod
    def samples(cls):
        return cls._get_service(service_name='samples')
    
    @classmethod
    def predict(cls):
        return cls._get_service(service_name='predict')
    
    
    #############################################################
    # The code below here is a self-contained class function 
    # and doesn't need to be modified.

    _instance = None
        
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ServiceManager, cls).__new__(cls)
            # Dictionary for service registration
            cls._instance._services = {}
            # Service initialization (initial loading into web service) function
            cls._instance._init_services()
            logs(code='manager')
        return cls._instance
            
    @classmethod
    def get_instance(cls):
        return cls._instance
    
    @classmethod
    def _get_service(cls, service_name=None):
        return cls._instance._services.get(service_name)
        