from flask import Blueprint, render_template
from frog.christmas_tree_monster import some_tips_please_sir


app = Blueprint('app', __name__, url_prefix='/')


@app.route('/')
def root():
    tips = some_tips_please_sir()
    return render_template('index.html', preloaded_tips={'tips': tips})
