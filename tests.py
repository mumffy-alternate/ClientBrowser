#!python
import os
import unittest
from datetime import datetime, timedelta

from config import basedir
from app import app, db
from app.models import User, Post
from app.forms import ProfileForm

class BasicTests(unittest.TestCase):
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

    def test_follow(self):
        u1 = User(nickname='a', email='a@mail.com')
        u2 = User(nickname='b', email='b@mail.com')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        self.assertIsNone(u1.unfollow(u2))

        u = u1.follow(u2)
        db.session.add(u)
        db.session.commit()
        self.assertIsNone(u1.follow(u2))
        self.assertTrue(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 1)
        self.assertEqual(u1.followed.first().nickname, 'b')
        self.assertEqual(u2.followers.count(), 1)
        self.assertEqual(u2.followers.first().nickname, 'a')

        u = u1.unfollow(u2)
        self.assertIsNotNone(u)
        db.session.add(u)
        db.session.commit()
        self.assertFalse(u1.is_following(u2))
        self.assertEquals(u1.followed.count(), 0)
        self.assertEquals(u2.followers.count(), 0)

    def test_follow_multiple(self):
        u1 = User(nickname='a', email='a@mail.com')
        u2 = User(nickname='b', email='b@mail.com')
        u3 = User(nickname='c', email='c@mail.com')
        u4 = User(nickname='d', email='d@mail.com')
        db.session.add(u1)
        db.session.add(u2)
        db.session.add(u3)
        db.session.add(u4)
        db.session.commit()

        u1.follow(u2)
        u1.follow(u3)
        u = u1.follow(u4)
        db.session.add(u)
        db.session.commit()
        self.assertTrue(u1.is_following(u2))
        self.assertTrue(u1.is_following(u3))
        self.assertTrue(u1.is_following(u4))
        self.assertEqual(u1.followed.count(), 3)

        u = u1.unfollow(u2)
        self.assertIsNotNone(u)
        db.session.add(u)
        db.session.commit()
        self.assertFalse(u1.is_following(u2))
        self.assertEquals(u1.followed.count(), 2)
        self.assertEquals(u2.followers.count(), 0)

        u1.unfollow(u3)
        u = u1.unfollow(u4)
        self.assertIsNotNone(u)
        db.session.add(u)
        db.session.commit()
        self.assertFalse(u1.is_following(u3))
        self.assertFalse(u1.is_following(u4))
        self.assertEquals(u1.followed.count(), 0)
        self.assertEquals(u3.followers.count(), 0)
        self.assertEquals(u4.followers.count(), 0)

        u1.unfollow(u3)
        u1.unfollow(u3)
        u1.unfollow(u4)
        u = u1.unfollow(u4)
        self.assertIsNone(u)

    def test_followed_by_multiple(self):
        u1 = User(nickname='a', email='a@mail.com')
        u2 = User(nickname='b', email='b@mail.com')
        u3 = User(nickname='c', email='c@mail.com')
        u4 = User(nickname='d', email='d@mail.com')
        db.session.add(u1)
        db.session.add(u2)
        db.session.add(u3)
        db.session.add(u4)
        db.session.commit()

        u2.follow(u1)
        u3.follow(u1)
        u = u4.follow(u1)
        self.assertIsNotNone(u)
        db.session.add(u)
        db.session.commit()
        self.assertEquals(u1.followers.count(), 3)

        u1.follow(u2)
        u = u1.follow(u3)
        db.session.add(u)
        db.session.commit()
        self.assertEquals(u1.followed.count(), 2)
        self.assertEquals(u1.followers.count(), 3)

    def test_follow_posts(self):
        u1 = User(nickname='a', email='a@mail.com')
        u2 = User(nickname='b', email='b@mail.com')
        u3 = User(nickname='c', email='c@mail.com')
        u4 = User(nickname='d', email='d@mail.com')
        db.session.add(u1)
        db.session.add(u2)
        db.session.add(u3)
        db.session.add(u4)

        utcnow = datetime.utcnow()
        p1 = Post(body="post from a", author=u1, timestamp=utcnow+timedelta(seconds=1))
        p2 = Post(body="post from b", author=u2, timestamp=utcnow+timedelta(seconds=2))
        p3 = Post(body="post from c", author=u3, timestamp=utcnow+timedelta(seconds=3))
        p4 = Post(body="post from d", author=u4, timestamp=utcnow+timedelta(seconds=4))
        p3a = Post(body="post A from c", author=u3, timestamp=utcnow+timedelta(seconds=13))
        p3b = Post(body="post B from c", author=u3, timestamp=utcnow+timedelta(seconds=23))
        db.session.add(p1)
        db.session.add(p2)
        db.session.add(p3)
        db.session.add(p4)
        db.session.add(p3a)
        db.session.add(p3b)
        db.session.commit()

        u1.follow(u1)
        u1.follow(u2)
        u1.follow(u4)
        u2.follow(u2)
        u2.follow(u3)
        u3.follow(u3)
        u3.follow(u4)
        u4.follow(u4)
        db.session.add(u1)
        db.session.add(u2)
        db.session.add(u3)
        db.session.add(u4)
        db.session.commit()

        f1 = u1.get_followed_posts().all()
        f2 = u2.get_followed_posts().all()
        f3 = u3.get_followed_posts().all()
        f4 = u4.get_followed_posts().all()
        self.assertEquals(len(f1), 3)
        self.assertEquals(len(f2), 4)
        self.assertEquals(len(f3), 4)
        self.assertEquals(len(f4), 1)
        self.assertItemsEqual(f1, [p1, p2, p4])
        self.assertItemsEqual(f2, [p2, p3, p3a, p3b])
        self.assertItemsEqual(f3, [p3, p4, p3a, p3b])
        self.assertItemsEqual(f4, [p4])

if __name__ == '__main__':
    unittest.main()