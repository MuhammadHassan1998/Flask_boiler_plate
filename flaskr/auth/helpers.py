from flaskr.models.user import User
from flaskr.models import db
from flask import session


def get_curr_user():
    user_id = session['user_id']
    return db.session.get(User, user_id)
