import re

from flask import Blueprint, render_template
from frog.christmas_tree_monster import some_tips_please_sir


endpoint = Blueprint('gary', __name__, url_prefix='/~GARY')


class GermanTranslator(object):

    mapping = [
        (r'\bA\b', 'EINE'),
        (r'\bOR\b', 'ODER'),
        (r'\bWITH\b', 'MIT'),
        (r'\bFROM\b', 'VON'),
        (r'\bIS NOT\b', 'KEINE'),
        (r'\bAND\b', 'UND'),
        (r'\bTHE\b', 'DIE'),
        (r'\bYOUR\b', 'DEINE'),
        (r'\bDO NOT\b', 'NEIMALS'),
        (r'\bIS\b', 'IST'),
        (r'\bTHIS\b', 'DIESES'),
    ]

    def translate(self, text):
        # Deutsch it inefficiently but hilariously
        for find, replace in self.mapping:
            text = re.sub(find, replace, text)
        return text


@endpoint.route('/<path:whatever>')
def frog_manual(whatever):
    translator = GermanTranslator()
    tips = [tip['tip'] for tip in some_tips_please_sir()]
    translated = list(map(translator.translate, tips))

    return render_template('gary/das_ist_mein_frog.html', tips=translated)
