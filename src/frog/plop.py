import re

from flask import Blueprint, render_template
from frog.christmas_tree_monster import some_tips_please_sir


endpoint = Blueprint('gary', __name__, url_prefix='/GARY')

@endpoint.route('/DE/MANUAL_2//DAS_IST_MEIN_FROG.ASPX')
def frog_manual():
    raw_tips = some_tips_please_sir()
    mapping = [
        ('W', 'V'),
        (r'\bTHE\b', 'DIE'),
        (r'\bYOUR\b', 'DEINE'),
        (r'\bDO NOT\b', 'NEIMALS'),
        (r'\bIS\b', 'IST'),
        (r'\bTHIS\b', 'DIESES'),
    ]

    # Deutsch it inefficiently.
    tips = []
    for tip in raw_tips:
        tip = tip.tip
        for find, replace in mapping:
            tip = re.sub(find, replace, tip)
        tips.append(tip)

    return render_template('gary/das_ist_mein_frog.html', tips=tips)
