from flask import Blueprint

ranking = Blueprint('ranking', __name__, template_folder='templates')

@ranking.route('/')
def ranking_page():
    return "Ranking page"