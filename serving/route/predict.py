from flask import jsonify, request, json
from flask.views import MethodView
from werkzeug.exceptions import HTTPException

import aidds.sys.http_codes as hc
import aidds.sys.messages as msg
from aidds.sys.utils.logs import route_error_logs as logs
from aidds.sys.utils.exception import AppException
from aidds.serving.service.service_manager import ServiceManager

sm = ServiceManager().get_instance()


class Predict(MethodView): 
    
    def post(self):
        try:
            try:
                # Exception handling is ambiguous
                # input_json = request.json
                input_data = request.get_data()
                input_json = json.loads(input_data)
            except ValueError as ve:
                logs(ve)
                error_message = eval(f'msg.exception.web.bad_json') + f': {ve}'
                return jsonify({'error': error_message}), hc.BR
            
            ret_json = sm.predict().run(in_json=input_json)
            return jsonify(ret_json), hc.OK
        except HTTPException as he:
            logs(he)
            error_message = eval(f'msg.exception.hc_msg.e{he.code}')
            return jsonify({'error': error_message}), he.code
        except AppException as ae:
            ae.print()
            error_message = msg.log.hc_msg.ise
            return jsonify({'error': error_message}), hc.ISE
        except Exception as e:
            logs(e)
            error_message = msg.log.hc_msg.ise
            return jsonify({'error': error_message}), hc.ISE