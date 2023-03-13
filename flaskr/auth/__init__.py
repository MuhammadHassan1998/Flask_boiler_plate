from flask import Blueprint
from flask_restful import Resource, Api
from .views import *
from .decorators import user_required

auth_bp = Blueprint('auth_bp', __name__, url_prefix='/api/auth', template_folder='templates',
                    static_folder='static')

api = Api(auth_bp)


api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')
api.add_resource(Register, '/register', endpoint='register')
api.add_resource(ForgotPassword, '/forgotpassword', endpoint='forgotpassword')
api.add_resource(ConfirmEmail, '/confirmemail', endpoint='confirmemail')