import tempfile
import os


DATABASE_URL = 'sqlite:///{0}'.format(os.path.join(tempfile.gettempdir(), 'testing.sqlite').replace('\\', '/'))
PROPAGATE_EXCEPTIONS = True
DEBUG = True
SQLALCHEMY_TRACK_MODIFICATIONS = False

DEBUG_SSL_CERT = os.environ['FLASK_DEBUG_SSL_CERT']
DEBUG_SSL_KEY = os.environ['FLASK_DEBUG_SSL_KEY']
MASTER_AUTH_PHRASE = os.environ['FLASK_MASTER_AUTH_PHRASE']

STATIC_SITE = os.path.abspath(os.path.join(os.path.dirname(__file__), '../static'))
