from flask import Blueprint, render_template, request

ranking = Blueprint('ranking', __name__, template_folder='templates')

@ranking.route('/')
def ranking_page():
    return render_template('ranking.html')