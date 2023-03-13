from flask import Blueprint
from flask_restful import Api
from .views import *

user_bp = Blueprint('user_bp', __name__, url_prefix='/api/user', template_folder='templates',
                    static_folder='static')

api = Api(user_bp)


api.add_resource(Users, '/users', endpoint='getusers')
api.add_resource(FriendRequest, '/sendrequest', endpoint='sendrequest')
api.add_resource(GetFriendRequest, '/getrequest', endpoint='getfriendrequests')
