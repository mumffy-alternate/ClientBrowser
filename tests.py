#!python
import os
import unittest

from config import basedir
from app import app, db
from app.models import User
from app.forms import ProfileForm

class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_changing_email_to_dupe_is_invalid(self):
        jojo = User(nickname='jojo', email='jojo@example.com')
        db.session.add(jojo)
        abobo = User(nickname='abobo', email='abobo@example.com')
        db.session.add(abobo)
        db.session.commit()

        with app.app_context():

            form = ProfileForm(jojo.email)
            form.email.data = abobo.email

            self.assertFalse(form.validate())
            self.assertGreater(len(form.email.errors), 0)
            self.assertNotEquals(str(form.email.errors[0]).find("This e-mail address is already in use.  Please provide a different one."), -1)

if __name__ == '__main__':
    unittest.main()