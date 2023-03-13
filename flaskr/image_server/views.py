from flask_restful import Resource
from flaskr.models.user import Photo
from flask import send_from_directory
from flaskr.auth.decorators import user_required
from flask import current_app


class Image(Resource):
    @user_required
    def get(self, id):
        from flaskr import photos
        url = photos.url(id)
        photo = Photo.query.filter_by(
            filename=url).first()
        path = current_app.root_path
        path = path.replace('flaskr','')
        path = path+'images'
        if photo:
            return send_from_directory(path, id)
        else:
            return {"no": "image"}
