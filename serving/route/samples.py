from flask import jsonify, request, abort, json
from flask.views import MethodView
from werkzeug.exceptions import HTTPException

import aidds.sys.http_codes as hc
import aidds.sys.messages as msg
from aidds.sys.utils.logs import route_error_logs as logs
from aidds.sys.utils.exception import AppException
from aidds.serving.service.service_manager import ServiceManager

sm = ServiceManager().get_instance()


class Samples(MethodView):
    
    def get(self):
        try:
            recommend_count = request.args.get('req_cnt', default=3, type=int)
            sample = sm.samples().get(recommend_count=recommend_count)
            # Test HTTPException
            # abort(401)
            return jsonify(sample), hc.OK
        except HTTPException as he:
            logs(he)
            error_message = eval(f'msg.exception.hc_msg.e{he.code}')
            return jsonify({'error': error_message}), he.code
        except AppException as ae:
            ae.print()
            error_message = msg.exception.hc_msg.e500
            return jsonify({'error': error_message}), hc.ISE
        except Exception as e:
            logs(e)
            error_message = msg.exception.hc_msg.e500
            return jsonify({'error': error_message}), hc.ISE
        
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
            return jsonify(input_json), hc.OK
        except HTTPException as he:
            logs(he)
            error_message = eval(f'msg.exception.hc_msg.e{he.code}')
            return jsonify({'error': error_message}), he.code
        except AppException as ae:
            ae.print()
            error_message = msg.exception.hc_msg.e500
            return jsonify({'error': error_message}), hc.ISE
        except Exception as e:
            logs(e)
            error_message = msg.exception.hc_msg.e500
            return jsonify({'error': error_message}), hc.ISE