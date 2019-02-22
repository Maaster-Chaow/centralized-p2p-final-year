from flask import g

from server import create_app
from server.models import db, User
from server.mail import mail, send_mail
from server.customs import pending_regs

def test_config():
    assert not create_app().testing
    assert create_app('testing').testing

def test_app_db():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        user = User(email_id='something@example.com',
                    pub_key=b'w'*100, username='susan',)
        db.session.add(user)
        db.session.commit()
        assert User.query.filter_by(username='susan').first() is not None

def test_app_mail():
    app = create_app('testing')
    with app.app_context():
        with mail.record_messages() as outbox:
            send_mail(['something@example.com'],
                      'testing', 'testing',
                      '<br>testing</br>')
            assert len(outbox) == 1
            assert outbox[0].subject == 'testing'

def test_app_reg_cache():
    app = create_app('testing')
    with app.app_context():
        pending_regs.set(1,2)
        assert pending_regs.get(1) == 2