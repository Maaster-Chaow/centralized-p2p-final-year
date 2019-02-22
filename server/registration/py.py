import json
import datetime
import random

from flask import request, escape, session, render_template

from server import app, db
from server.models import User
from server.utils import send_mail, make_response_msg


MAX_TRY = 3
OTP_STR_LEN = 32
OTP_DIGITS = 6


@app.route('/register', methods=['POST'])
def register():
    json_data = request.get_json()
    email_id = json_data.get('email_id')
    username = json_data.get('username')
    if email_id and username:
        user = User.query.filter_by(email_id=email_id).first()
        
        # if user is present delete
        # and continue same as new user
        if user:
            db.session.delete(user)
            db.session.commit()
        
        # if not then create a session for the user
        # to be confirmed later.
        # The session consists of:
        # 1. emaid_id
        # 2. username
        # 3. OTP
        # 4. time of registration request.
        # 5. counter
        otpstr = ''.join(str(random.choice(range(0,9))) for i in range(OTP_STR_LEN))
        otp = int(otpstr) % 10**OTP_DIGITS
        session[email_id] = dict(email_id=email_id, username=username,
                                 time=datetime.datetime.utcnow(),
                                 counter=MAX_TRY, otp=otp)
        user = dict(email_id=email_id, username=username, otp=otp)
        # send otp through email
        send_mail(subject='Email confirmation', recipients=[email_id],
                  text_body=render_template('otp_email.txt', user=user),
                  html_body=render_template('otp_email.html', user=user))
        return make_response_msg(status='ok',
                                 msg='otp sent to email-id, awaiting confirmation.')
    return make_response_msg(status='error', msg='data not in proper format.')