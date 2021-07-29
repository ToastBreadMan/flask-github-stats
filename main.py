from flask import Flask
from ranking import ranking
from registration import register

app = Flask(__name__)

app.register_blueprint(ranking)
app.register_blueprint(register, url_prefix='/register')