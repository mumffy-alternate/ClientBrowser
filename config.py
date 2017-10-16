import os
basedir = os.path.abspath(os.path.dirname(__file__))

WTF_CSRF_ENALBED=True
SECRET_KEY = 'blah blah blah'

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')