from flask import jsonify, request
from flask.views import MethodView
from werkzeug.exceptions import HTTPException

import aidds.sys.http_code as hc
from aidds.sys.utils.logs import route_error_logs as logs
from aidds.sys.utils.exception import AiddsException
from aidds.serving.service.service_manager import ServiceManager

sm = ServiceManager().get_instance()


class Predict(MethodView):
    
    def post(self):
        try:
            input_json = request.json
            pred_result_dict = sm.predict().run(input_json=input_json)
            return jsonify(pred_result_dict), hc.OK
        except HTTPException as he:
            logs(he)
            return jsonify({'error': str(he)}), he.code
        except AiddsException as ae:
            ae.print()
            return jsonify({'error': str(ae)}), hc.INTERNAL_SERVER_ERROR
        except Exception as e:
            logs(e)
            return jsonify({'error': str(e)}), hc.INTERNAL_SERVER_ERROR