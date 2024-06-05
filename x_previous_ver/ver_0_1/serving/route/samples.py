from flask import jsonify, request
from flask.views import MethodView
from werkzeug.exceptions import HTTPException

import aidds_buy.serving.route.return_code as rc
from aidds_buy.sys.utils import AiddsServiceException as ASE
from aidds_buy.serving.service.service_manager import ServiceManager

sm = ServiceManager()


class Samples(MethodView):
    def get(self):
        try:
            sample_cnt = request.args.get('s_cnt', default=3, type=int)
            samples = sm.samples().get(sample_cnt=sample_cnt)
            return jsonify(samples), rc.OK
        except HTTPException as he:
            sm.logs().mid(code='ERROR', value=f'[GET] {he}', name=__name__)
            return jsonify({'error': str(he)}), he.code
        except ASE as ae:
            sm.logs().mid(code='ERROR', value=f'[GET]{ae}', name=__name__)
            return jsonify({'error': str(ae)}), rc.INTERNAL_SERVER_ERROR
        except Exception as e:
            sm.logs().mid(code='ERROR', value=f'[GET] {e}', name=__name__)
            return jsonify({'error': str(e)}), rc.INTERNAL_SERVER_ERROR
        
    def post(self):
        try:
            json_data = request.json
            return jsonify(json_data), rc.OK
        except HTTPException as he:
            sm.logs().mid(code='ERROR', value=f'[POST] {he}', name=__name__)
            return jsonify({'error': str(he)}), he.code
        except Exception as e:
            sm.logs().mid(code='ERROR', value=f'[POST] {e}', name=__name__)
            return jsonify({'error': str(e)}), rc.INTERNAL_SERVER_ERROR
 