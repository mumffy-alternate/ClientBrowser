from sqlalchemy import select
from sqlalchemy.orm import backref

from app import db

followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime)
    followed = db.relationship(
        'User',
        secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'),
        lazy='dynamic'
    )

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
            return self

    def follow_self_if_not_already(self):
        if not self.is_following_self():
            self.follow(self)
            db.session.add(self)
            db.session.commit()

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
            return self

    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    def get_followed_posts(self):
        return Post.query \
            .join(followers, (followers.c.followed_id == Post.user_id)) \
            .filter(followers.c.follower_id == self.id) \
            .order_by(Post.timestamp.desc())

    def is_following_self(self):
        query = select([followers.c.follower_id]) \
            .where(followers.c.followed_id == self.id) \
            .where(followers.c.follower_id == self.id)
        results = db.session.execute(query).fetchall()
        if len(results) == 1:
            return True
        return False

    @classmethod
    def get_by_nickname(cls, nickname):
        return cls.query.filter_by(nickname=nickname).first()

    @property
    def is_authenticated(self):  # misleading name? means this User is *allowed* to authenticate?
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python2
        except NameError:
            return str(self.id)  # python3

    def __repr__(self):
        return '<User {0}>'.format(self.nickname)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {0}>'.format(self.body)


class Case(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date_opened = db.Column(db.DateTime)
    date_closed = db.Column(db.DateTime)
    case_name = db.Column(db.String(255), unique=True)
    court_case_number = db.Column(db.String(255))
    clients = db.relationship('Person', back_populates='case', lazy='dynamic')
    phone_logs = db.relation('PhoneLogEntry', back_populates='case', lazy='dynamic')

    def get_name_front(self):
        return str(self.case_name).split('/')[0]

    def get_name_back(self):
        return str(self.case_name).split('/')[1]


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    address_line1 = db.Column(db.String(255))
    address_line2 = db.Column(db.String(255))
    address_city = db.Column(db.String(255))
    address_state = db.Column(db.String(2))
    address_postal_code = db.Column(db.String(30))
    address_country = db.Column(db.String(3))
    birthdate = db.Column(db.DateTime)
    sex = db.Column(db.String(15))  # TODO change to FK or something
    case_id = db.Column(db.Integer, db.ForeignKey('case.id'))
    case = db.relationship('Case',
                           back_populates='clients')  # TODO can one Person be invovled in multiple cases?  i.e. many-to-many?
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    role = db.relationship('Role', back_populates='people')
    role_comment = db.Column(db.String(127))


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String(127), unique=True)
    short_name = db.Column(db.String(127), unique=True, nullable=False)
    people = db.relationship('Person', back_populates='role', lazy='dynamic')


class PhoneLogEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    content = db.Column(db.Text)
    caller_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    caller = db.relationship('Person')
    case_id = db.Column(db.Integer, db.ForeignKey('case.id'), nullable=False)
    case = db.relationship('Case', back_populates='phone_logs')


class LegacyPhoneLog(db.Model):
    case_name = db.Column(db.String(255), unique=True, primary_key=True)
    content = db.Column(db.Text)
    extraction_time = db.Column(db.DateTime, nullable=False)
    case = db.relationship('Case', primaryjoin=(Case.case_name == case_name),
                           foreign_keys=case_name, backref=backref('legacy_phone_log', uselist=False))
