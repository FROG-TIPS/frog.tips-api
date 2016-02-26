from flask import Blueprint, render_template, abort
from frog.christmas_tree_monster import some_tips_please_sir, just_a_tip_oof_right_there


app = Blueprint('app', __name__, url_prefix='/')


@app.route('', defaults={'number': None})
@app.route('<int:number>')
def root(number):
    if number is not None:
        tip = just_a_tip_oof_right_there(number)
        if tip is None:
            return abort(404)

        tips = [tip]
    else:
        tips = some_tips_please_sir()

    return render_template('index.html', preloaded_tips={'tips': tips})
