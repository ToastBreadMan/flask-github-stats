import json

from flask import Blueprint, request, render_template, redirect
from database import redis_server

register = Blueprint('register', __name__, template_folder='templates')

#TODO: in order for it to run make real json
@register.route('/', methods=['GET', 'POST'])
def register_page():
    if request.method == "POST":
        data = request.json
        redis_server.set(data['name'], json.dumps(data))
        redis_server.publish("newuser", "new user has joined")
        return redirect("/")
    else:
        return render_template("register.html")