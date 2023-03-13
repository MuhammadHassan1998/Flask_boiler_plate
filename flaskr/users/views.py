from flaskr.models.user import User, FriendRequests
from flask_restful import Resource
from flaskr.models import db
from flaskr.auth.decorators import *
from flask import request, make_response, render_template
from flaskr.auth.helpers import get_curr_user


class Users(Resource):
    @user_required
    def get(self):
        curr_user = get_curr_user()
        users = User.query.all()
        list_users = []
        for user in users:
            if user.email != curr_user.email and (user not in curr_user.aspiredfriends and user not in curr_user.desiredfriends):
                list_users.append(user)
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('showusers.html', users=list_users), 200, headers)


class FriendRequest(Resource):
    @user_required
    def post(self):
        to_user_id = request.form.get('user_id', None)
        curr_user = get_curr_user()
        friendrequest = FriendRequests.query.filter_by(
            from_user=curr_user.userid, to_user=to_user_id).first()
        if friendrequest:
            return {"user": "success"}, 200
        new_request = FriendRequests(
            from_user=curr_user.userid, to_user=to_user_id, status="send")
        db.session.add(new_request)
        db.session.commit()
        return {"user": "success"}, 200


class GetFriendRequest(Resource):
    @user_required
    def get(self):
        curr_user = get_curr_user()
        friendrequests = FriendRequests.query.filter_by(
            to_user=curr_user.userid).all()
        user_ids = []
        for frequest in friendrequests:
            user_ids.append(frequest.from_user)
        users = User.query.filter(User.userid.in_(user_ids)).all()
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('showfriendrequests.html', users=users), 200, headers)

    @user_required
    def post(self):
        curr_user = get_curr_user()
        from_user_id = request.form.get('user_id', None)
        from_user = User.query.filter_by(userid=from_user_id).first()
        curr_user.aspiredfriends.append(from_user)
        friendrequests = FriendRequests.query.filter_by(
            from_user=from_user_id, to_user=curr_user.userid).first()
        db.session.delete(friendrequests)
        db.session.add(curr_user)
        db.session.commit()
        return {"user": "success"}, 200
