from flask import jsonify, request
from flask.views import MethodView
from werkzeug.exceptions import HTTPException

import aidds_buy.sys.http_code as hc
from aidds_buy.sys.utils.logs import route_error_logs as logs
from aidds_buy.sys.utils.exception import AiddsException
from aidds_buy.serving.service.service_manager import ServiceManager

sm = ServiceManager().get_instance()


class Samples(MethodView):
    
    def get(self):
        try:
            sample_count = request.args.get('s_cnt', default=3, type=int)
            samples = sm.samples().get(sample_count=sample_count)
            return jsonify(samples), hc.OK
        except HTTPException as he:
            logs(he)
            return jsonify({'error': str(he)}), he.code
        except AiddsException as ae:
            ae.print()
            return jsonify({'error': str(ae)}), hc.INTERNAL_SERVER_ERROR
        except Exception as e:
            logs(e)
            return jsonify({'error': str(e)}), hc.INTERNAL_SERVER_ERROR
        
    def post(self):
        try:
            json_data = request.json
            return jsonify(json_data), hc.OK
        except HTTPException as he:
            logs(he)
            return jsonify({'error': str(he)}), he.code
        except AiddsException as ae:
            ae.print()
            return jsonify({'error': str(ae)}), hc.INTERNAL_SERVER_ERROR
        except Exception as e:
            logs(e)
            return jsonify({'error': str(e)}), hc.INTERNAL_SERVER_ERROR
            
            

