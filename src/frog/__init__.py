from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_envvar('FLASK_CONFIG')
db = SQLAlchemy()


@app.errorhandler(404)
def page_not_found(e):
    return render_template('frogerror.html'), 404


@app.after_request
def injoke(res):
    res.headers['FROG'] = 'FROG IS FULLY HYPERTEXT COMPATIBLE'
    res.headers['Bay-Area'] = 'log off; yak shaving; python tire fire; gentrifrogcation'
    res.headers['Everybody-Back-In-The-Box'] = "fuckin' headers are full of ladybugs man"
    return res


import frog.poking
frog.poking.init_db(app, db)

import frog.boners
app.register_blueprint(frog.boners.app)

import frog.enclave
app.register_blueprint(frog.enclave.api)

import frog.plop
app.register_blueprint(frog.plop.endpoint)

if __name__ == "__main__":
    app.run()
