from .main import db
import enum


class RoleType(enum.Enum):
    admin = "Admin User"
    user = "Client User"


friendship = db.Table('friends',
                      db.Column('fk_user_from', db.Integer, db.ForeignKey(
                          'user.userid'), primary_key=True),
                      db.Column('fk_user_to', db.Integer, db.ForeignKey(
                          'user.userid'), primary_key=True)
                      )


class User(db.Model):
    userid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.LargeBinary(1000), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    phoneno = db.Column(db.String(10))
    gender = db.Column(db.String(7))
    default_profile_image = db.Column(db.String(1000))
    default_cover_image = db.Column(db.String(1000))
    profile_image = db.Column(db.String(1000))
    cover_image = db.Column(db.String(1000))
    photos = db.relationship('Photo', cascade='all, delete')
    role = db.Column(db.Enum(RoleType), nullable=False)
    desiredfriends = db.relationship('User',
                                     secondary=friendship,
                                     primaryjoin=(
                                         friendship.c.fk_user_from == userid),
                                     secondaryjoin=(
                                         friendship.c.fk_user_to == userid),
                                     lazy='dynamic', cascade='all, delete')
    aspiredfriends = db.relationship('User',
                                     secondary=friendship,
                                     primaryjoin=(
                                         friendship.c.fk_user_to == userid),
                                     secondaryjoin=(
                                         friendship.c.fk_user_from == userid),
                                     lazy='dynamic', cascade='all, delete')
    posts = db.relationship('UserPost', cascade='all, delete')
    pages = db.relationship('Page', cascade='all, delete')
    groups = db.relationship('Group', cascade='all, delete')

    def __repr__(self):
        return '<User %r>' % self.username


class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    filename = db.Column(db.String(1000))
    user_id = db.Column(db.Integer, db.ForeignKey(User.userid), nullable=False)


class StatusType(enum.Enum):
    send = "Request Send"
    pending = "Request Pending"
    accepted = "Request Sccepted"
    rejected = "Request Rejected"


class FriendRequests(db.Model):
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    from_user = db.Column(db.Integer, db.ForeignKey(
        'user.userid'), nullable=False)
    to_user = db.Column(db.Integer, db.ForeignKey(
        'user.userid'), nullable=False)
    status = db.Column(db.Enum(StatusType), nullable=False)
