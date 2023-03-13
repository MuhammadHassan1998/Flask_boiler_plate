from celery import Celery

celery = Celery(__name__, broker='redis://localhost:6379')


@celery.task
def send_mail(user):
    return "good"