from flask import Flask

from aidds_buy.serving.route.samples import Samples
from aidds_buy.serving.route.predict import Predict


app = Flask(__name__)

# 플라스크 정의
app.debug = True 

# 라우터 정의
app.add_url_rule('/samples', view_func=Samples.as_view('samples'))
app.add_url_rule('/predict', view_func=Predict.as_view('predict'))