from flask import Flask

from aidds.serving.route.samples import Samples
# from aidds.serving.route.predict import Predict


app = Flask(__name__)

app.add_url_rule('/samples', view_func=Samples.as_view('samples'))
# app.add_url_rule('/predict', view_func=Predict.as_view('predict'))