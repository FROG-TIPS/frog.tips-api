import tempfile
import os


DATABASE_URL = 'sqlite:///{0}'.format(os.path.join(tempfile.gettempdir(), 'testing.sqlite').replace('\\', '/'))
PROPAGATE_EXCEPTIONS = True
DEBUG = True
SQLALCHEMY_TRACK_MODIFICATIONS = False
