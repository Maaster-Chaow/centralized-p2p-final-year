from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()
migrate = Migrate()


class User(db.Model):
    '''User schema for database.
    The fields are given as follows:
    1. phone_no: User phone number acquired on registration.
    2. username: Name of user submitted during registration.
    3. pub_key: public key of user.'''
    _username_length = 20
    _email_id_length = 256
    id = db.Column(db.Integer, primary_key=True)
    #phone_no = db.Column(db.String(10), index=True, unique=True)
    email_id = db.Column(db.String(_email_id_length),
                         index=True, unique=True)
    username = db.Column(db.String(_username_length), index=True)
    pub_key = db.Column(db.LargeBinary(2048))
    register_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    
    def __repr__(self):
        return '<User {}: {}>'.format(self.username, self.phone_no)