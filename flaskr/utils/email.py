from flask_mail import Message


def send_email(to_user, subject, body):
    from flaskr import mail
    msg = Message(subject=subject, sender="hassan@facebook.com",
                  recipients=[to_user, ])
    msg.body = body
    mail.send(msg)
    return "send"
