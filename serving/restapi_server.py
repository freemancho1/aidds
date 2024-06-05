from flask import Flask

from aidds_buy.serving import samples_route
from aidds_buy.serving import predict_route

app = Flask(__name__)

app.add_url_rule('/samples', view_func=samples_route.as_view('samples'))
app.add_url_rule('/predict', view_func=predict_route.as_view('predict'))