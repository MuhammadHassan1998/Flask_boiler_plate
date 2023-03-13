from flask import Blueprint
from flask_restful import Api
from .views import *

imageserver_bp = Blueprint('imageserver_bp', __name__, url_prefix='/_uploads/photos', template_folder='templates',
                    static_folder='static')

api = Api(imageserver_bp)
api.add_resource(Image, '/<id>', endpoint='image')