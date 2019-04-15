import pytest
import json

#from flask import g

from server import create_app
from server.models import db
from server.customs import pending_regs
from server.mail import mail
from server.config import OTP_TIME_OUT


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

# user sends email and username info to tracking server
# for registration.
def test_register(client, app):
    response = client.post('/registration/register', json={
            'username':'susan', 'email_id': 'something@nothing.com'
        }
    )
    assert response.status_code == 200
    #assert 'http://localhost/registration/register' == response.headers['Location']
    assert response.get_json()['status'] == 'ok'


# The server creates a session for the user request to be authenticated later.
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

# The server sends an otp to the user for confirmation.
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

# Send a certificate signing signing request, to the server.
def test_cert_signing(client, app):
    from cryptography import x509
    from cryptography.x509.oid import NameOID
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives.asymmetric import rsa
    
    key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend())

    client_info = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, u"IN"),
        x509.NameAttribute(NameOID.)
        
