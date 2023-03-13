from .main import db
from .user import User
from .group import *
from .page import *
import enum


class PostType(enum.Enum):
    userpost = "User Timeline"
    grouppost = "Created in Group"
    pagepost = "Created by page"
    sharedpagepost = "Shared by user from page"
    shareduserpost = "shared by user from user"
    sharedgrouppost = "shared by user from group"


likes = db.Table('like',
                 db.Column('user_id', db.Integer, db.ForeignKey(
                     'user.userid', onupdate='CASCADE', ondelete='CASCADE'), primary_key=True),
                 db.Column('post_id', db.Integer, db.ForeignKey(
                     'post.postid', onupdate='CASCADE', ondelete='CASCADE'), primary_key=True)
                 )


class Post(db.Model):
    postid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    postcontent = db.Column(db.String(250))
    type = db.Column(db.Enum(PostType), nullable=False)
    likes = db.relationship('User',
                            secondary=likes,
                            primaryjoin=(
                                likes.c.post_id == postid),
                            secondaryjoin=(
                                likes.c.user_id == User.userid),
                            lazy='dynamic', cascade='all, delete')
    comments = db.relationship("PostComment", cascade='all, delete')
    __mapper_args__ = {
        "polymorphic_identity": "post",
        "polymorphic_on": type,
    }


class UserPost(Post):
    postid = db.Column(db.Integer, db.ForeignKey(Post.postid),
                       primary_key=True)
    created_by = db.Column('created_by', db.ForeignKey(
        User.userid, onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    __mapper_args__ = {
        "polymorphic_identity": "userpost",
    }


class SharedUserPost(UserPost):
    postid = db.Column(db.Integer, db.ForeignKey(UserPost.postid),
                       primary_key=True)
    shared_by = db.Column('shared_by', db.ForeignKey(
        User.userid, onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    __mapper_args__ = {
        "polymorphic_identity": "shareduserpost",
    }


class GroupPost(UserPost):
    postid = db.Column(db.Integer, db.ForeignKey(UserPost.postid),
                       primary_key=True)
    group_id = db.Column('group_id', db.ForeignKey(
        Group.groupid, onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    __mapper_args__ = {
        "polymorphic_identity": "grouppost",
    }


class SharedGroupPost(GroupPost):
    postid = db.Column(db.Integer, db.ForeignKey(GroupPost.postid),
                       primary_key=True)
    shared_by = db.Column('shared_by', db.ForeignKey(
        User.userid, onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    __mapper_args__ = {
        "polymorphic_identity": "sharedgrouppost",
    }


class PagePost(Post):
    postid = db.Column(db.Integer, db.ForeignKey(Post.postid),
                       primary_key=True)
    created_by = db.Column('created_by', db.ForeignKey(
        Page.pageid, onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    __mapper_args__ = {
        "polymorphic_identity": "pagepost",
    }


class SharedPagePost(PagePost):
    postid = db.Column(db.Integer, db.ForeignKey(PagePost.postid),
                       primary_key=True)
    shared_by = db.Column('shared_by', db.ForeignKey(
        User.userid, onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    __mapper_args__ = {
        "polymorphic_identity": "sharedpagepost",
    }
