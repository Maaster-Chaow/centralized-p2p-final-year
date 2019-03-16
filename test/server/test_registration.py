import pytest
import json

#from flask import g

from server import create_app
from server.models import db
from server.customs import pending_regs
from server.mail import mail
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
    with app.app_context():
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

def test_register(client, app):
    response = client.post('/registration/register', json={
            'username':'susan', 'email_id': 'something@nothing.com'
        }
    )
    assert response.status_code == 200
    #assert 'http://localhost/registration/register' == response.headers['Location']
    assert response.get_json()['status'] == 'ok'

def test_registration_otp_email_sending(client, app):
    with app.app_context():
        with mail.record_messages() as outbox:
            response = client.post('/registration/register', json={
                    'username':'susan', 'email_id': 'something@nothing.com'
                }
            )
            assert len(outbox) == 1
            assert 'Email' in outbox[0].subject

@pytest.mark.parametrize(('email_id', 'username', 'status', 'msg'), (
    ('', '', 'error', 'no data, data required'),
    ('', 'something', 'error', 'email_id required'),
    ('abc@def.com', '', 'error', 'username required'),
    ('abcefgh', 'abc', 'error', 'invalid email_id'),
    ('abc@def.com', 'abc', 'ok', 'otp sent to email_id, awaiting confirmation')
))
def test_registration_validate_input(client, email_id, username, status, msg):
    response = client.post('/registration/register',
                json={'email_id': email_id, 'username': username})
    assert response.get_json() == {'status': status, 'msg': msg}

def test_registration_pending(client, app):
    req1 = dict(email_id='abc@def.com', username='abc')
    req2 = dict(email_id='ghi@jkl.com', username='ghi')
    req3 = req1
    with app.app_context():
        client.post('/registration/register', json=req1)
        client.post('/registration/register', json=req2)
        rsp = client.post('/registration/register', json=req3)
        assert rsp.get_json() == {'status': 'error',
                                  'msg': 'registration pending, awaiting confirmation'}
        assert pending_regs.size() == 2
        assert pending_regs.ttl == OTP_TIME_OUT

#@pytest.mark.parametrize(('email_id', 'pub_key', 'otp', 'status', 'msg'), (
#    ('', '', '', 'error', 'no data, data required'),
#    ('', '', )
#))
    