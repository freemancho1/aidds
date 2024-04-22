# The display order is very important in __init__.py
# - The module that is called first must be listed at the bottom.
#
from .service.predict.preprocessing \
    import PredictPreprocessing as preprocessing
from .service.samples import Samples as samples_service
from .service.predict.predict import Predict as predict_service
    
from .service.service_manager import ServiceManager as service_manager

from .route.samples import Samples as samples_route
from .route.predict import Predict as predict_route

from .restapi_server import create_app