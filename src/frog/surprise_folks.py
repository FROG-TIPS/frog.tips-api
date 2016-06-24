import functools

from flask import abort, request, redirect, Blueprint, Response, current_app, render_template, Response
import flask.json
import jsonpatch

from frog.christmas_tree_monster import open_sesame, \
    genie_remember_this_phrase, genie_forget_this_phrase, \
    genie_share_your_knowledge, TipMaster, \
    PhraseError, CramTipError, SearchTipError, QueryTipError, BulkUpdateTipError, UpdateTipError

from frog.high_score import ApiError, BaseApiResponse


secret_api = Blueprint('secret_api', __name__, url_prefix='/api/2')
tip_master = TipMaster()


######## TOP SECRET ########
# DO NOT LOOK BELOW THIS LINE
# I'M WARNING YOUSE, MISTER
# AW YOU DID IT, YA FAT IDIOT


def api_response(data=None, status=None):
    return BaseApiResponse(data=data, status=status)


class try_or_hint(object):
    def __init__(self, hint):
        self.hint = hint

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except ApiError as e:
                raise e
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
        return api_response(data={'phrase': phrase, 'id': id})
    except PhraseError as e:
        raise ApiError(message=str(e))


@secret_api.route('/auth/revoke', methods=['POST'])
@try_or_hint('{"id": "[EXTREME GILBERT GOTTFRIED VOICE] AUTH PHRASE ID"}')
def revoke_auth():
    phrase_id = get_json('id')
    genie_forget_this_phrase(phrase_id)
    return api_response(data={'status': 'REVOKED.'})


@secret_api.route('/auth/', methods=['GET'])
def list_auth():
    try:
        knowledge = genie_share_your_knowledge()
        return api_response(data={'knowledge': knowledge})
    except PhraseError as e:
        raise ApiError(message=str(e))


@secret_api.route('/tips/search', methods=['POST'])
@try_or_hint('{"tip": "YOUR FAT DUMB SEARCH CRITERIA (TEXT; OPTIONAL)", "approved": "TIPS THAT HAVE BEEN APPROVED (BOOLEAN; OPTIONAL)", "tweeted": "TIPS THAT HAVE BEEN TWEETED (BOOLEAN; OPTIONAL)"}')
def search():
    json = request.get_json(force=True, silent=True)
    fields = ('tip', 'approved', 'tweeted')
    query = dict(zip(fields, map(json.get, fields)))
    return api_response(data={'results': tip_master.search_for_spock(query)})


## FULLY AUTOMATE YOUR FROG WITH THIS APE-Y EYE.

@secret_api.route('/tips', methods=['POST', 'PATCH'])
def give_tip():
    if request.method == 'POST':
        try:
            text = get_json('tip')
            number = tip_master.cram_tip(text)
            return api_response(data={'number': number})
        except Exception:
            raise ApiError(message='FULLY CAPITALIZED TIP MENTIONING FROG WITH FULL STOP.')

    elif request.method == 'PATCH':
        try:
            patch = jsonpatch.JsonPatch(request.get_json(force=True, silent=True))
            results = tip_master.its_not_a_goth_phase(patch=patch)
            return api_response(data=results)
        except Exception as e:
            raise ApiError(message="SEE THIS: http://jsonpatch.com/. VALID OPS ARE replace, VALID PATHS ARE /{number}/approved AND /{number}/tweeted")


@secret_api.route('/tips/<int:num>', methods=['GET'])
def get_tip(num):
    tip = tip_master.just_the_tip(num, super_secret_info=True, approved_only=False)

    if tip is None:
        # Sorry, you don't get our wonderful 404 page
        return api_response(status=404)
    else:
        return api_response(data=tip)


@secret_api.route('/tips/<int:num>', methods=['PATCH'])
@try_or_hint('SEE THIS: http://jsonpatch.com/. VALID OPS ARE replace, VALID PATHS ARE /approved AND /tweeted')
def frog_approves_of_your_tip_young_man(num):
    patch = jsonpatch.JsonPatch(request.get_json(force=True, silent=True))
    tip_master.its_not_a_phase(num, patch=patch)
    return api_response(data={'status': "OKAY, SURE."})
