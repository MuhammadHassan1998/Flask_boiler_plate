from flask_restful import Resource
from flaskr.models import db
from flaskr.models.user import Photo
from flask import request, make_response, render_template, redirect
from flaskr.auth.decorators import user_required
from flaskr.auth.helpers import get_curr_user


class HomePage(Resource):
    @user_required
    def get(self):
        user = get_curr_user()
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('home.html', user=user), 200, headers)


class UpdateUserPhoto(Resource):
    @user_required
    def get(self):
        user = get_curr_user()
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('updatephotos.html', user=user), 200, headers)

    @user_required
    def post(self):
        from flaskr import photos
        uploaded_file = request.files['file']
        user = get_curr_user()
        if uploaded_file:
            image_type = request.form.get('upload')
            filename = photos.save(uploaded_file)
            url = photos.url(filename)
            photo = Photo(filename=url, user_id=user.userid)
            user.photos.append(photo)
            if image_type == "profile":
                user.profile_image = url
            else:
                user.cover_image = url
            db.session.add(user)
            db.session.commit()

        return redirect("homepage")
