from .main import db
from .user import User


pagefollower = db.Table('pagefollower',
                        db.Column('user_id', db.ForeignKey(
                            'user.userid', onupdate='CASCADE', ondelete='CASCADE'), primary_key=True),
                        db.Column('page_id', db.ForeignKey(
                            'page.pageid', onupdate='CASCADE', ondelete='CASCADE'), primary_key=True),
                        )


pagelikes = db.Table('pagelike',
                     db.Column('user_id', db.ForeignKey(
                         'user.userid', onupdate='CASCADE', ondelete='CASCADE'), primary_key=True),
                     db.Column('page_id', db.ForeignKey(
                         'page.pageid', onupdate='CASCADE', ondelete='CASCADE'), primary_key=True),
                     )


class Page(db.Model):
    pageid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pagedescription = db.Column(db.String(2500))
    created_by = db.Column('created_by', db.ForeignKey(
        User.userid, onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    pagename = db.Column(db.String(250), nullable=False)
    page_cover_image = db.Column(db.String(10))
    page_profile_image = db.Column(db.String(10))
    followers = db.relationship('User',
                                secondary=pagefollower,
                                primaryjoin=(
                                    pagefollower.c.page_id == pageid),
                                secondaryjoin=(
                                    pagefollower.c.user_id == User.userid),
                                lazy='dynamic', cascade='all, delete')
    likes = db.relationship('User',
                            secondary=pagelikes,
                            primaryjoin=(
                                pagelikes.c.page_id == pageid),
                            secondaryjoin=(
                                pagelikes.c.user_id == User.userid),
                            lazy='dynamic', cascade='all, delete')
    posts = db.relationship('PagePost', cascade='all, delete')