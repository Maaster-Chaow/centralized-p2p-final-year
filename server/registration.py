import random

#from flask import current_app as app
from flask import (
    request, render_template, g, Blueprint
)

from .models import User
from server.mail import send_mail, make_response_msg
from .config import MAX_OTP_RETRY, OTP_TRUN_STR_LEN, OTP_SIZE


bp = Blueprint('regis', __name__, url_prefix='/registration')


@bp.route('/register', methods=['POST'])
def register():
    json_data = request.get_json()
    email_id = json_data.get('email_id')
    username = json_data.get('username')
    if email_id and username:
        if email_id in g.pending_registration:
            return make_response_msg(status='error',
                msg='registration request in progress, awaiting confirmation.')
        # create a session for the user to be confirmed later.
        # The session consists of:
        # 1. emaid_id
        # 2. username
        # 3. OTP
        # 4. time of registration request.
        # 5. counter
        otpstr = ''.join(str(random.choice(range(0,9))) for i in range(OTP_TRUN_STR_LEN))
        otp = int(otpstr) % 10**OTP_SIZE
        g.pending_registration.set(email_id, dict(username=username,
                            counter=MAX_OTP_RETRY, otp=otp))
        user = dict(email_id=email_id, username=username, otp=otp)
        # send otp through email
        send_mail(subject='Email confirmation', recipients=[email_id],
                  text_body=render_template('otp_email.txt', user=user),
                  html_body=render_template('otp_email.html', user=user))
        return make_response_msg(status='ok',
                                 msg='otp sent to email-id, awaiting confirmation.')
    return make_response_msg(status='error', msg='data not in proper format.')