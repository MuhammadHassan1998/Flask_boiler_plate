from flaskr.models.user import User
from flask_restful import Resource
from flaskr.models import db
from .decorators import *
from flask import request, make_response, render_template, redirect, url_for
from flask import session
import bcrypt
from sqlalchemy.exc import IntegrityError
from flaskr.utils.email import send_email
from dotenv import load_dotenv
import os
from itsdangerous import URLSafeTimedSerializer

load_dotenv()
serializer = URLSafeTimedSerializer(os.getenv('SECRET_KEY'))


class Login(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('login.html'), 200, headers)

    def post(self):
        email = request.form.get('email')
        password = request.form.get('password')
        if not email:
            return 'Missing email', 400
        if not password:
            return 'Missing password', 400

        user = User.query.filter_by(email=email).first()
        if not user:
            return 'User Not Found!', 404
        if bcrypt.checkpw(password.encode('utf-8'), user.password):
            session['email'] = email
            session['user_id'] = user.userid
            return redirect(url_for('home_bp.homepage'))
        return 'Password does not match', 404


class Register(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('register.html'), 200, headers)

    def post(self):
        try:
            email = request.form.get('email', None)
            password = request.form.get('password', None)
            username = request.form.get('name', None)
            #dateofbirth = request.form.get('dateofbirth', None)
            if not email:
                return 'Missing email', 400
            if not password:
                return 'Missing password', 400
            if not username:
                return 'Missing username', 400
            # if not dateofbirth:
            #     return 'Missing dateofbirth', 400
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            user = User(email=email, password=hashed,
                        username=username,
                        dob='2000-01-01',
                        role='user',
                        default_profile_image='https://bootdey.com/img/Content/avatar/avatar7.png',
                        default_cover_image='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ1R8MsfkjK6Vl1MNJARv12hHNRl9crGE5GVw&usqp=CAU')
            db.session.add(user)
            db.session.commit()

            return redirect("login")
        except IntegrityError:
            db.session.rollback()
            return 'User Already Exists', 400
        except AttributeError:
            return 'Provide an Email and Password in JSON format in the request body', 400


class Logout(Resource):
    @user_required
    def get(self):
        session.pop('email', None)
        return redirect(url_for('auth_bp.login'))


class ForgotPassword(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('resetrequest.html'), 200, headers)

    def post(self):
        email = request.form.get('email', None)
        if not email:
            return 'email must be given', 400
        user = User.query.filter_by(email=email).first()
        if not user:
            return 'no user exists with this email', 400
        subject = "Confirm your email"
        token = serializer.dumps(email, salt='email-confirm-key')
        confirm_url = url_for(
            'auth_bp.confirmemail',
            token=token,
            _external=True)

        message = f'''
            TO Reset Your Password Click on the Link Given Below
            {confirm_url}
        '''
        send_email(email, subject, message)
        return "email send", 200


class ConfirmEmail(Resource):
    def get(self):
        token = request.args.get('token', None)
        token = token[0:len(token)-1]
        try:
            email = serializer.loads(token, salt="email-confirm-key", max_age=48600)
        except:
            abort(404)

        user = User.query.filter_by(email=email).first()
        if not user:
            return "user not verified", 400
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('resetpassword.html', user=user), 200, headers)

    def post(self):
        id = request.form.get('username', None)
        password = request.form.get('password', None)
        if not id:
            return "wrong request", 400
        user = User.query.filter_by(userid=id).first()
        if not user:
            return "No user exists", 400
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        user.password = hashed
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth_bp.login'))
