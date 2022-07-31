from flask import Flask

app = Flask(__name__)

import flask_crud_app.views

app.run(debug=True, port=8008)
