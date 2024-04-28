from flask import jsonify, request, abort, json
from flask.views import MethodView
from werkzeug.exceptions import HTTPException

from aidds.sys import http_codes as hc
from aidds.sys import messages as msg
from aidds.sys.utils import route_error_logs as logs
from aidds.sys.utils import app_exception
from aidds.serving import service_manager

sm = service_manager().get_instance()


class Samples(MethodView):
    
    def get(self):
        try:
            recommend_count: int = request.args.get('req_cnt', default=3, type=int)
            zero_data: int = request.args.get('zero_data', default=0, type=int)
            req_list_str: str = request.args.get('req_list', default='[]')
            req_list = list(map(str, req_list_str.strip('[]').split(',')))
            sample = sm.samples().get(
                recommend_count = recommend_count, 
                zero_data = zero_data,
                req_list = req_list
            )
            # Test HTTPException
            # abort(401)
            return sample, hc.OK
        except HTTPException as he:
            logs(he)
            error_message = eval(f'msg.exception.hc_msg.e{he.code}')
            return jsonify({'error': error_message}), he.code
        except app_exception as ae:
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
            return input_json, hc.OK
        except HTTPException as he:
            logs(he)
            error_message = eval(f'msg.exception.hc_msg.e{he.code}')
            return jsonify({'error': error_message}), he.code
        except app_exception as ae:
            ae.print()
            error_message = msg.exception.hc_msg.e500
            return jsonify({'error': error_message}), hc.ISE
        except Exception as e:
            logs(e)
            error_message = msg.exception.hc_msg.e500
            return jsonify({'error': error_message}), hc.ISE