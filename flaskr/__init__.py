from flask import Flask, redirect, url_for
from .config import DevelopmentConfig, TestingConfig
from .models.main import db
from flask_migrate import Migrate
from .auth import auth_bp
from .home import home_bp
from .users import user_bp
from .image_server import imageserver_bp
from celery import Celery
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask_mail import Mail


migrate = Migrate()
mail = Mail()
photos = UploadSet('photos', IMAGES)


def create_app(test_config=None):
    app = Flask(__name__)
    if test_config is None:
        app.config.from_object(DevelopmentConfig())
        configure_uploads(app, photos)
        app.register_blueprint(auth_bp)
        app.register_blueprint(home_bp)
        app.register_blueprint(imageserver_bp)
        app.register_blueprint(user_bp)
        db.init_app(app)
        migrate.init_app(app=app, db=db)
        mail.init_app(app)

        @app.route("/")
        def redirect_to_login():
            return redirect(url_for('auth_bp.login'))
    else:
        app.config.from_object(TestingConfig())
        app.register_blueprint(auth_bp)
        app.register_blueprint(home_bp)
        db.init_app(app)
    return app
