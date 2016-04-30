from flask import abort, request, redirect, Blueprint, Response, current_app
import flask.json

from frog.christmas_tree_monster import the_search_for_spock, open_sesame, \
    genie_remember_this_phrase, genie_forget_this_phrase, PhraseError

from frog.high_score import ApiError


secret_api = Blueprint('secret_api', __name__, url_prefix='/api/2')


######## TOP SECRET ########
# DO NOT LOOK BELOW THIS LINE
# I'M WARNING YOUSE, MISTER
# AW YOU DID IT, YA FAT IDIOT


@secret_api.before_request
def before_request():
    # DON'T SNOOP ON ME OR MY SON EVER AGAIN
    if request.url.startswith('http://'):
        url = request.url.replace('http://', 'https://', 1)
        return redirect(url, code=301)

    if request.content_length > 1024:
        raise ApiError(
            message='FROG CANNOT EXCEED MAXIMUM SIZE IN GIRTH, WIDTH OR LENGTH.',
            status_code=413)

    master_phrase = current_app.config['MASTER_AUTH_PHRASE']
    phrase = request.headers.get('Authorization')

    if not open_sesame(master_phrase, phrase):
        raise ApiError(
            message='FROG EXPECTED Authorization HEADER.',
            status_code=401)


@secret_api.route('/auth/add', methods=['POST'])
def add_auth():
    phrase = genie_remember_this_phrase()
    return flask.json.jsonify(phrase=phrase)


@secret_api.route('/auth/revoke', methods=['POST'])
def revoke_auth():
    try:
        data = request.get_json(force=True, silent=True)
        phrase = data['phrase']
        genie_forget_this_phrase(phrase)
        return flask.json.jsonify(status='revoked')
    except Exception as e:
        raise ApiError.as_json_hint(
            '{"phrase": "[EXTREME GILBERT GOTTFRIED VOICE] AUTH PHRASE"}')


@secret_api.route('/search', methods=['POST'])
def search():
    try:
        data = request.get_json(force=True, silent=True)
        query = data['query']
        return flask.json.jsonify(results=the_search_for_spock(query))
    except Exception:
        raise ApiError.as_json_hint(
            '{"query": "YOUR FAT DUMB SEARCH CRITERIA"}')
