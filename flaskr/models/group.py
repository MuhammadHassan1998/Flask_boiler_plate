from .main import db
from .user import User


groupmembers = db.Table('groupmember',
                        db.Column('user_id', db.ForeignKey(
                            'user.userid', onupdate='CASCADE', ondelete='CASCADE'), primary_key=True),
                        db.Column('group_id', db.ForeignKey(
                            'group.groupid', onupdate='CASCADE', ondelete='CASCADE'), primary_key=True),
                        )


class Group(db.Model):
    groupid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    groupdescription = db.Column(db.String(2500))
    created_by = db.Column('created_by', db.ForeignKey(
        User.userid, onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    groupname = db.Column(db.String(250), nullable=False)
    group_cover_image = db.Column(db.String(10))
    group_profile_image = db.Column(db.String(10))
    members = db.relationship('User',
                              secondary=groupmembers,
                              primaryjoin=(
                                  groupmembers.c.group_id == groupid),
                              secondaryjoin=(
                                  groupmembers.c.user_id == User.userid),
                              lazy='dynamic', cascade='all, delete')
    posts = db.relationship('GroupPost', cascade='all, delete')
