import pytest
from flaskr import create_app, db
from flaskr.models.user import *


@pytest.fixture(scope="module")
def app():
    app = create_app(test_config=True)
    with app.test_request_context():
        db.create_all()
    yield app
    with app.test_request_context():
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
