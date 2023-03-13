from flask import Blueprint
from flask_restful import Api
from .views import *

home_bp = Blueprint('home_bp', __name__, url_prefix='/api/home', template_folder='templates',
                    static_folder='static')

api = Api(home_bp)

api.add_resource(HomePage, '/homepage', endpoint='homepage')
api.add_resource(UpdateUserPhoto, '/updateuserphotos', endpoint='updateuserphotos')