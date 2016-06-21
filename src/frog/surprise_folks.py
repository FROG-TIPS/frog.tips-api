import functools

from flask import abort, request, redirect, Blueprint, Response, current_app, render_template
import flask.json

from frog.christmas_tree_monster import open_sesame, \
    genie_remember_this_phrase, genie_forget_this_phrase, \
    genie_share_your_knowledge, TipMaster, \
    PhraseError, CramTipError, SearchTipError, QueryTipError

from frog.high_score import ApiError


secret_api = Blueprint('secret_api', __name__, url_prefix='/api/2')
tip_master = TipMaster()


######## TOP SECRET ########
# DO NOT LOOK BELOW THIS LINE
# I'M WARNING YOUSE, MISTER
# AW YOU DID IT, YA FAT IDIOT


class try_or_hint(object):
    def __init__(self, hint):
        self.hint = hint

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception:
                raise ApiError.as_json_hint(self.hint)

        return wrapper


def get_json(key):
    return request.get_json(force=True, silent=True)[key]


@secret_api.before_request
def before_request():
    # DON'T SNOOP ON ME OR MY SON EVER AGAIN
    if request.url.startswith('http://'):
        url = request.url.replace('http://', 'https://', 1)
        return redirect(url, code=301)

    content_length = request.content_length

    if content_length is not None and content_length > 1024:
        raise ApiError(
            message='FROG CANNOT EXCEED MAXIMUM SIZE IN GIRTH, WIDTH OR LENGTH.',
            status_code=413)

    master_phrase = current_app.config['MASTER_AUTH_PHRASE']
    phrase = request.headers.get('Authorization')

    if not open_sesame(master_phrase, phrase):
        raise ApiError(
            message='FROG EXPECTED Authorization HEADER.',
            status_code=401)


@secret_api.route('/')
def help():
    return render_template('api2doc.txt')


@secret_api.route('/auth/add', methods=['POST'])
@try_or_hint('{"comment": "DESCRIBE WHY YOU DECIDED TO LET YET ANOTHER PERSON IN ON THE SECRET"}')
def add_auth():
    try:
        comment = get_json('comment')
        phrase, id = genie_remember_this_phrase(comment)
        return flask.json.jsonify(phrase=phrase, id=id)
    except PhraseError as e:
        raise ApiError(message=str(e))


@secret_api.route('/auth/revoke', methods=['POST'])
@try_or_hint('{"id": "[EXTREME GILBERT GOTTFRIED VOICE] AUTH PHRASE ID"}')
def revoke_auth():
    phrase_id = get_json('id')
    genie_forget_this_phrase(phrase_id)
    return flask.json.jsonify(status='REVOKED.')


@secret_api.route('/auth/', methods=['GET'])
def list_auth():
    try:
        knowledge = genie_share_your_knowledge()
        return flask.json.jsonify(knowledge=knowledge)
    except PhraseError as e:
        raise ApiError(message=str(e))

@secret_api.route('/search', methods=['POST'])
@try_or_hint('{"query": "YOUR FAT DUMB SEARCH CRITERIA", "approved_only": "true OR false TO SEARCH ONLY APPROVED TIPS. DEFAULT TO true."}')
def search():
    json = request.get_json(force=True, silent=True)
    query = json['query']
    approved_only = json.get('approved_only', True)
    return flask.json.jsonify(results=tip_master.search_for_spock(query, approved_only=approved_only))


## FULLY AUTOMATE YOUR FROG WITH THIS APE-Y EYE.

@secret_api.route('/tips', methods=['POST'])
@try_or_hint('{"text": "FULLY CAPITALIZED TIP MENTIONING FROG WITH FULL STOP."}')
def give_tip():
    text = get_json('text')
    number = tip_master.cram_tip(text)
    return flask.json.jsonify(number=number)


@secret_api.route('/tips/<int:num>', methods=['GET'])
def get_tip(num):
    tip = tip_master.just_the_tip(num, super_secret_info=True, approved_only=False)

    if tip is None:
        # Sorry, you don't get our wonderful 404 page
        return abort(404)
    else:
        return flask.json.dumps(tip)


@secret_api.route('/tips/<int:num>/<any(approve,disapprove):method>', methods=['PATCH'])
@try_or_hint('DESPITE THIS BEING A PATCH METHOD, IT TAKES NO DATA.')
def frog_approves_of_your_tip_young_man(num, method):
    if method == 'approve':
        approve = True
    elif method == 'disapprove':
        approve = False
    else:
        return abort(404)

    tip_master.approve_of_your_child(num, approve=approve)
    return flask.json.jsonify(status='OKAY, SURE.')
