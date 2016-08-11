import os

MASTER_AUTH_PHRASE = 'CROAKING'

os.environ['FLASK_CONFIG'] = os.path.join(os.path.dirname(__file__), '../src/frog/config/test.py')
os.environ['FLASK_MASTER_AUTH_PHRASE'] = MASTER_AUTH_PHRASE


def test_i_can_import_this_even():
    from frog import app
