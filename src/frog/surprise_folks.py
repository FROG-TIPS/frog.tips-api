import functools

from flask import abort, request, redirect, Blueprint, Response, current_app, render_template, Response
import flask.json
import jsonpatch

from frog.christmas_tree_monster import open_sesame, \
    genie_remember_this_phrase, genie_forget_this_phrase, \
    genie_share_your_knowledge, TipMaster, \
    PhraseError, CramTipError, SearchTipError, QueryTipError, UpdateTipError

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


class restrict_to(object):
    def __init__(self, perms):
        self.perms = perms

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            master_phrase = current_app.config['MASTER_AUTH_PHRASE']
            phrase = request.headers.get('Authorization')

            if not open_sesame(master_phrase, phrase, self.perms):
                raise ApiError(
                    message='FROG EXPECTED Authorization HEADER. ALTERNATIVELY, YOU MAY NOT HAVE PERMISSION TO ACCESS THIS.',
                    status_code=401)

            return func(*args, **kwargs)

        return wrapper


def get_json(key):
    return request.get_json(force=True, silent=True)[key]


@secret_api.before_request
def before_request():
    content_length = request.content_length

    if content_length is not None and content_length > 1024:
        raise ApiError(
            message='FROG CANNOT EXCEED MAXIMUM SIZE IN GIRTH, WIDTH OR LENGTH.',
            status_code=413)


@secret_api.route('/')
@restrict_to(['read'])
def help():
    return render_template('api2doc.txt')


@secret_api.route('/auth/add', methods=['POST'])
@restrict_to(['auth.add'])
@try_or_hint('{"comment": "DESCRIBE WHY YOU DECIDED TO LET YET ANOTHER PERSON IN ON THE SECRET", "perms": "AN ARRAY OF PERMISSIONS"}')
def add_auth():
    try:
        comment = get_json('comment')
        perms = get_json('perms')
        phrase, id = genie_remember_this_phrase(comment, perms)
        return api_response(data={'phrase': phrase, 'id': id})
    except PhraseError as e:
        raise ApiError(message=str(e))


@secret_api.route('/auth/revoke', methods=['POST'])
@restrict_to(['auth.del'])
@try_or_hint('{"id": "[EXTREME GILBERT GOTTFRIED VOICE] AUTH PHRASE ID"}')
def revoke_auth():
    phrase_id = get_json('id')
    genie_forget_this_phrase(phrase_id)
    return api_response(data={'status': 'REVOKED.'})


@secret_api.route('/auth/', methods=['GET'])
@restrict_to(['auth.read'])
def list_auth():
    try:
        knowledge = genie_share_your_knowledge()
        return api_response(data={'knowledge': knowledge})
    except PhraseError as e:
        raise ApiError(message=str(e))


@secret_api.route('/tips/search', methods=['POST'])
@restrict_to(['tips.search'])
@try_or_hint('{"tip": "YOUR FAT DUMB SEARCH CRITERIA (TEXT; OPTIONAL)", "approved": "TIPS THAT HAVE BEEN APPROVED (BOOLEAN; OPTIONAL)", "tweeted": "TIPS THAT HAVE BEEN TWEETED (BOOLEAN; OPTIONAL)"}')
def search():
    json = request.get_json(force=True, silent=True)
    fields = ('tip', 'approved', 'tweeted', 'moderated')
    query = dict(zip(fields, map(json.get, fields)))
    return api_response(data={'results': tip_master.search_for_spock(query)})


## FULLY AUTOMATE YOUR FROG WITH THIS APE-Y EYE. TIPS OUT FOR HARAMBE.

@secret_api.route('/tips', methods=['POST'])
@restrict_to(['tips.add'])
@try_or_hint('FULLY CAPITALIZED TIP MENTIONING FROG WITH FULL STOP.')
def give_tip():
    text = get_json('tip')
    number = tip_master.cram_tip(text)
    return api_response(data={'number': number})


@secret_api.route('/tips', methods=['GET'])
@restrict_to(['tips.read'])
@try_or_hint('THIS DOES NOT TAKE ANY PARAMETERS SO I HAVE NO IDEA HOW YOU MESSED IT UP.')
def a_croak_of_tips_my_good_man():
    return api_response(tip_master.some_tips(super_secret_info=True, approved_only=False))


@secret_api.route('/tips', methods=['PATCH'])
@restrict_to(['tips.mod'])
@try_or_hint("SEE THIS: http://jsonpatch.com/. VALID OPS ARE replace, VALID PATHS ARE /{number}/approved, /{number}/tip AND /{number}/tweeted")
def bulk_tips():
    patch = jsonpatch.JsonPatch(request.get_json(force=True, silent=True))
    results = tip_master.its_not_a_goth_phase(patch=patch)
    return api_response(data=results)


@secret_api.route('/tips/<int:num>', methods=['GET'])
@restrict_to(['tips.read'])
def get_tip(num):
    tip = tip_master.just_the_tip(num, super_secret_info=True, approved_only=False)

    if tip is None:
        # Sorry, you don't get our wonderful 404 page
        return api_response(status=404)
    else:
        return api_response(data=tip)
