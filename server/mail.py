'''Utility module'''
from threading import Thread

from flask import current_app
from flask_mail import Mail, Message

from .config import ADMINS_EMAIL


mail = Mail()


def validate_email():
    pass

def concurrent(f):
    '''Start a thread in background.'''
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()
    return wrapper


@concurrent
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_mail(recipients, subject, text_body, html_body):
    msg = Message(subject, sender=ADMINS_EMAIL[0],
                  recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    send_async_email(current_app._get_current_object(), msg)


def make_response_msg(status, msg, **kwargs):
    resp = dict(status=status, msg=msg)
    for name,value in kwargs.items():
        resp[name] = value
    return resp