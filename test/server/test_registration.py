import pytest
import json

from flask import jsonify

from server import app, app_config, db, mail
from server.utils import make_response_msg


@pytest.fixture
def client():
    app.config.from_object(app_config['testing'])
    client = app.test_client()
    mail.init_app(app)
    with app.app_context():
        # initialize database
        db.create_all()
    yield client
    
    db.session.remove()
    db.drop_all()

def test_register(client):
    data = dict(email_id='something@example.com', username='susan')
    with mail.record_messages() as outbox:
        rv = client.post('/register', json=data)
        assert json.loads(rv.data.decode()) == make_response_msg('ok',
            'otp sent to email-id, awaiting confirmation.')
        assert len(outbox) == 1
        assert outbox[0].subject == 'Email confirmation'
    