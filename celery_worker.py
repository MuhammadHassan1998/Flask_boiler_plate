import os
from flaskr import create_app
from flaskr.celery_tasks import celery

app = create_app()
app.app_context().push()