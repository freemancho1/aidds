from flask import Flask

from aidds_buy.serving.route.samples import Samples
from aidds_buy.serving.route.predict import Predict


app = Flask(__name__)

# 플라스크 설정 정의
# (이곳의 정의는 main.py에서 호출되는 tornado 설정에 의해 적용되지 않음)
app.debug = True

# 라우터 정의
app.add_url_rule('/samples', view_func=Samples.as_view('samples'))
app.add_url_rule('/predict', view_func=Predict.as_view('predict'))