import logging
import sys

from flask import Flask, jsonify, request, redirect
from flask_sqlalchemy import SQLAlchemy

from frog.high_score import ApiError


app = Flask(__name__)
app.config.from_envvar('FLASK_CONFIG')
app.config['JSONIFY_MIMETYPE'] = 'application/json;charset=utf-8'
app.config['TRAP_HTTP_EXCEPTIONS'] = True

app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.INFO)

db = SQLAlchemy(session_options={'autocommit': False, 'autoflush': False})


@app.errorhandler(ApiError)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.errorhandler(Exception)
def handle_all_api_crap(error):
    # Handle redirects
    try:
        if error.code >= 300 and error.code < 400:
            return error
    except AttributeError:
        pass

    try:
        body = {'status_code': error.code, 'message': (error.description or '').upper()}
    except Exception as e:
        app.logger.exception(e)
        body = {'status_code': 500, 'message': 'THERE WAS A PROBLEM HANDLING A PREVIOUS ERROR. REPORT THIS TO YOUR NEAREST BEARDED UNIX WIZARD.'}

    resp = jsonify(body)
    resp.status_code = body['status_code']
    return resp


@app.after_request
def injoke(res):
    res.headers['FROG'] = 'FROG IS FULLY HYPERTEXT COMPATIBLE'
    res.headers['Bay-Area'] = 'log off; yak shaving; python tire fire; gentrifrogcation'
    res.headers['Everybody-Back-In-The-Box'] = "fuckin' headers are full of ladybugs man"
    return res


import frog.poking
frog.poking.init_db(app, db)

import frog.enclave
app.register_blueprint(frog.enclave.api)

import frog.surprise_folks
app.register_blueprint(frog.surprise_folks.secret_api)

# FIXME: Re-enable if the gitlab static repo goes public again
## So this is happening
#if app.debug:
#    from flask import send_from_directory
#
#    @app.route('/', defaults={'path': 'index.html'})
#    @app.route('/<path:path>')
#    def send_file(path):
#        resp = send_from_directory(app.config['STATIC_SITE'], path)
#
#        # FUck me, right?
#        if path.lower().endswith('.aspx'):
#            resp.mimetype = 'text/html'
#
#        return resp
