import os
basedir = os.path.abspath(os.path.dirname(__file__))

WTF_CSRF_ENALBED=True
SECRET_KEY = 'blah blah blah'

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = False

MAIL_SERVER = 'localhost'
MAIL_PORT = 25
MAIL_USERNAME = None
MAIL_PASSWORD = None

ADMINS = ['you@example.com']

POSTS_PER_PAGE = 3