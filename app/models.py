from sqlalchemy import select

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
        secondary = followers,
        primaryjoin = (followers.c.follower_id == id),
        secondaryjoin = (followers.c.followed_id == id),
        backref = db.backref('followers', lazy='dynamic'),
        lazy = 'dynamic'
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
        return Post.query\
            .join(followers, (followers.c.followed_id == Post.user_id))\
            .filter(followers.c.follower_id == self.id)\
            .order_by(Post.timestamp.desc())

    def is_following_self(self):
        query = select([followers.c.follower_id])\
            .where(followers.c.followed_id == self.id)\
            .where(followers.c.follower_id == self.id)
        results = db.session.execute(query).fetchall()
        if len(results) == 1:
            return True
        return False

    @classmethod
    def get_by_nickname(cls, nickname):
        return cls.query.filter_by(nickname=nickname).first()

    @property
    def is_authenticated(self): # misleading name? means this User is *allowed* to authenticate?
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id) # python2
        except NameError:
            return str(self.id) # python3

    def __repr__(self):
        return '<User {0}>'.format(self.nickname)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {0}>'.format(self.body)