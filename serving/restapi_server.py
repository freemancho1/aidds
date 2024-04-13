from flask import Flask

from aidds.serving.route.samples import Samples


app = Flask(__name__)

app.add_url_rule('/samples', view_func=Samples.as_view('samples'))