from .main import db
from .user import *
from .posts import *


class PostComment(db.Model):
    commentid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column('user_id', db.ForeignKey(
        User.userid, onupdate='CASCADE', ondelete='CASCADE'))
    post_id = db.Column('post_id', db.ForeignKey(
        Post.postid, onupdate='CASCADE', ondelete='CASCADE'))
    comment_desc = db.Column(db.String(1000))
