from flask import Blueprint, render_template, abort
from frog.christmas_tree_monster import TipMaster


app = Blueprint('app', __name__, url_prefix='/')
tip_master = TipMaster()

@app.route('')
def root():
    tips = tip_master.some_tips()

    # DISPLAY THIS TIP IN THE META DESCRIPTION FOR ALL THE CHAT PROGRAMS KIDS ARE USING THESE DAYS
    titular_tip = tips[0]['tip'] if tips else None

    return render_template('index.html', preloaded_tips={'tips': tips}, titular_tip=titular_tip)
