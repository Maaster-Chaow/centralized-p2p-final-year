import pytest
import json

from flask import g

from server import create_app
from server.models import db
from server.utils import make_response_msg
from server.config import OTP_TIME_OUT


# @pytest.fixture
# def client():
#     app.config.from_object(app_config['testing'])
#     client = app.test_client()
#     mail.init_app(app)
#     with app.app_context():
#         # initialize database
#         g.regis_pending = Cache(ttl=OTP_TIME_OUT)
#         db.create_all()
#     yield client
#     
#     db.session.remove()
#     db.drop_all()

@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
    yield app
    db.session.remove()
    db.session.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

def test_register(client):
    data = dict(email_id='something@example.com', username='susan')
    baddata = dict(email_id='341jaaja', username='john')
    with mail.record_messages() as outbox:
        rv = client.post('/register', json=data)
        assert data['email_id'] in g.regis_pending
        assert json.loads(rv.data.decode()) == make_response_msg('ok',
            'otp sent to email-id, awaiting confirmation.')
        rv = client.post('/register', json=data)
        assert json.loads(rv.data.decode()) == make_response_msg('error',
            'registration request in progress, awaiting confirmation.')
        rv = client.post('/register', json=baddata)
        assert json.loads(rv.data.decode()) == make_response_msg('error',
            'bad user data')
        assert len(outbox) == 1
        assert outbox[0].subject == 'Email confirmation'
    