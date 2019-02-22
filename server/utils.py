'''Utility module'''
from threading import Thread

from flask_mail import Message

from server import app, mail
from server.config import ADMINS_EMAIL


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
    send_async_email(app, msg)


def make_response_msg(status, msg, **kwargs):
    resp = dict(status=status, msg=msg)
    for name,value in kwargs.items():
        resp[name] = value
    return resp