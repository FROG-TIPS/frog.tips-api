import os


database_url = os.environ['DATABASE_URL']

SQLALCHEMY_DATABASE_URI = database_url
PROPAGATE_EXCEPTIONS = True
