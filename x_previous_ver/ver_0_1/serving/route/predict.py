from flask import request, jsonify
from flask.views import MethodView
from werkzeug.exceptions import HTTPException

import aidds_buy.serving.route.return_code as rc
from aidds_buy.sys.utils import AiddsServiceException as ASE
from aidds_buy.serving.service.service_manager import ServiceManager

sm = ServiceManager()

class Predict(MethodView):
    
    def post(self):
        try:
            data = request.json
            _xx = sm.predict().run(data)
            
            return jsonify({'status': 'ok'}), rc.OK
        except HTTPException as he:
            sm.logs().mid(code='ERROR', value=f'[POST] {he}', name=__name__)
            return jsonify({'error': str(he)}), he.code
        except ASE as ae:
            sm.logs().mid(code='ERROR', value=f'[POST]{ae}', name=__name__)
            return jsonify({'error': str(ae)}), rc.INTERNAL_SERVER_ERROR
        except Exception as e:
            sm.logs().mid(code='ERROR', value=f'[POST] {e}', name=__name__)
            return jsonify({'error': str(e)}), rc.INTERNAL_SERVER_ERROR