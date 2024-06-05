from flask import Flask

from aidds_buy.serving.route.samples import Samples
from aidds_buy.serving.route.predict import Predict


app = Flask(__name__)

app.add_url_rule('/samples', view_func=Samples.as_view('samples'))
app.add_url_rule('/predict', view_func=Predict.as_view('predict'))