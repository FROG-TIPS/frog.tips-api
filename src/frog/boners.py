from flask import Blueprint, render_template, abort
from frog.christmas_tree_monster import some_tips_please_sir, just_a_tip_oof_right_there


app = Blueprint('app', __name__, url_prefix='/')


@app.route('')
def root():
    tips = some_tips_please_sir()

    # DISPLAY THIS TIP IN THE META DESCRIPTION FOR ALL THE CHAT PROGRAMS KIDS ARE USING THESE DAYS
    titular_tip = tips[0]['tip'] if tips else None

    return render_template('index.html', preloaded_tips={'tips': tips}, titular_tip=titular_tip)
