from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy

from frog.high_score import ApiError


app = Flask(__name__)
app.config.from_envvar('FLASK_CONFIG')
app.config['JSONIFY_MIMETYPE'] = 'application/json;charset=utf-8'

db = SQLAlchemy(session_options={'autocommit': False, 'autoflush': False})


@app.errorhandler(404)
def page_not_found(e):
    return render_template('frogerror.html'), 404


@app.errorhandler(ApiError)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.after_request
def injoke(res):
    res.headers['FROG'] = 'FROG IS FULLY HYPERTEXT COMPATIBLE'
    res.headers['Bay-Area'] = 'log off; yak shaving; python tire fire; gentrifrogcation'
    res.headers['Everybody-Back-In-The-Box'] = "fuckin' headers are full of ladybugs man"
    return res


import frog.poking
frog.poking.init_db(app, db)

import frog.plop
app.register_blueprint(frog.plop.endpoint)

import frog.boners
app.register_blueprint(frog.boners.app)

import frog.enclave
app.register_blueprint(frog.enclave.api)

import frog.surprise_folks
app.register_blueprint(frog.surprise_folks.secret_api)

if __name__ == "__main__":
    if app.debug:
        app.run(ssl_context=(app.config['DEBUG_SSL_CERT'], app.config['DEBUG_SSL_KEY']))
