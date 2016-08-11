import os

MASTER_AUTH_PHRASE = 'CROAKING'

os.environ['FLASK_CONFIG'] = os.path.join(os.path.dirname(__file__), '../config/test.py')
os.environ['FLASK_MASTER_AUTH_PHRASE'] = MASTER_AUTH_PHRASE

from frog import app
