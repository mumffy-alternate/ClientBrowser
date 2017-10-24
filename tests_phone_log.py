#!python
import os
import unittest
from datetime import datetime, timedelta

from config import basedir
from app import app, db
from app.models import Case, Person, Role, PhoneLogEntry

class PhoneLogTests(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()
        self.populate_sample_data()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def populate_sample_data(self):
        utcnow = datetime.utcnow()
        case = Case(case_name=r"Animal/Bunch", date_opened=utcnow)
        self.case = case
        self.update_db(case)

        a = Person(first_name="Andrew", last_name="Aardvark", case=case)
        b = Person(first_name="Bonnie", last_name="Badger", case=case)
        c = Person(first_name="Clyde",  last_name="Crocodile", case=case)
        self.people = {'a':a, 'b':b, 'c':c}
        self.update_db(a)
        self.update_db(b)
        self.update_db(c)

        log1 = PhoneLogEntry(timestamp=utcnow+timedelta(minutes=01), case=case, content="hello 01", caller=a)
        log2 = PhoneLogEntry(timestamp=utcnow+timedelta(minutes=02), case=case, content="hello 02", caller=a)
        log3 = PhoneLogEntry(timestamp=utcnow+timedelta(minutes=03), case=case, content="hello 03", caller=c)
        log4 = PhoneLogEntry(timestamp=utcnow+timedelta(minutes=04), case=case, content="hello 04", caller=a)

        self.update_db(log1)
        self.update_db(log2)
        self.update_db(log3)
        pass

    def update_db(self, entity):
        db.session.add(entity)
        db.session.commit()

    def test_basic(self):
        self.assertEquals(self.case.clients.count(), 3)

        client_first_names = [c.first_name for c in self.case.clients]
        self.assertItemsEqual(client_first_names, ['Andrew', 'Bonnie', 'Clyde'])

        self.assertEquals(self.case.phone_logs.count(), 4)
        logs = self.case.phone_logs.filter_by(caller=self.people['a']).all()
        self.assertEquals(len(logs), 3)

        log_contents = [l.content for l in logs]
        self.assertItemsEqual(log_contents, ['hello 01', 'hello 02', 'hello 04'])





if __name__ == '__main__':
    unittest.main()