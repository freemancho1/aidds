from flask import jsonify, request
from flask.views import MethodView
from werkzeug.exceptions import HTTPException

import aidds_buy.sys.http_code as hc
import aidds_buy.sys.message as msg
from aidds_buy.sys.utils.logs import route_error_logs as logs
from aidds_buy.sys.utils.exception import AiddsException
from aidds_buy.serving.service.service_manager import ServiceManager

sm = ServiceManager().get_instance()


class Predict(MethodView): 
    
    def post(self):
        try:
            input_json = request.json
            ret_json = sm.predict().run(in_json=input_json)
            return jsonify(ret_json), hc.OK
        except HTTPException as he:
            logs(he)
            error_message = eval(f'msg.log.hc_msg.e{he.code}')
            return jsonify({'error': error_message}), he.code
        except AiddsException as ae:
            ae.print()
            error_message = msg.log.hc_msg.ise
            return jsonify({'error': error_message}), hc.ISE
        except Exception as e:
            logs(e)
            error_message = msg.log.hc_msg.ise
            return jsonify({'error': error_message}), hc.ISE