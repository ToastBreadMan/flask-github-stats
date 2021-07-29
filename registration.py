from flask import Blueprint

register = Blueprint('register', __name__, template_folder='templates')

@register.route('/')
def register_page():
    return "Register page"