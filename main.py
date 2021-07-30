import json

import redis
from flask import Flask
from ranking import ranking
from registration import register
from flask_socketio import SocketIO
from database import redis_server
from github_functions import Function
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
socketio = SocketIO(app)

app.register_blueprint(ranking)
app.register_blueprint(register, url_prefix='/register')

pubsub = redis_server.pubsub()
pubsub.subscribe("data")


@socketio.on('message')
def handle_message(data):
    for item in pubsub.listen():
        try:
            print(item["data"].decode())
            socketio.emit("data", item["data"].decode())
        except Exception as e:
            print(e)


if __name__ == "__main__":
    socketio.run(app)