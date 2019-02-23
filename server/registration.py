import random

from validate_email import validate_email
from flask import (
    request, render_template, g, Blueprint
)

from .models import User
from .mail import send_mail
from .customs import make_response_msg, pending_regs
from .config import MAX_OTP_RETRY, OTP_TRUN_STR_LEN, OTP_SIZE


bp = Blueprint('regis', __name__, url_prefix='/registration')


@bp.route('/register', methods=['POST'])
def register():
    json_data = request.get_json()
    email_id = json_data.get('email_id')
    username = json_data.get('username')
    status, msg = 'ok', 'otp sent to email_id, awaiting confirmation'
    if not(username or email_id):
        status, msg = 'error', 'no data, data required'
    elif not email_id:
        status, msg = 'error', 'email_id required'
    elif not username:
        status, msg = 'error', 'username required'
    else:
        if not validate_email(email_id):
            status, msg = 'error', 'invalid email_id'
        elif email_id in pending_regs:
            status, msg = 'error', 'registration pending, awaiting confirmation'
        else:
        # create a session for the user to be confirmed later.
        # The session consists of:
        # 1. emaid_id
        # 2. username
        # 3. OTP
        # 4. time of registration request.
        # 5. counter
            otpstr = ''.join(str(random.choice(range(0,9))) for i in range(OTP_TRUN_STR_LEN))
            otp = int(otpstr) % 10**OTP_SIZE
            pending_regs.set(email_id, dict(username=username,
                                            counter=MAX_OTP_RETRY, otp=otp))
            user = dict(email_id=email_id, username=username, otp=otp)
        # send otp through email
            send_mail(subject='Email confirmation', recipients=[email_id],
                      text_body=render_template('otp_email.txt', user=user),
                      html_body=render_template('otp_email.html', user=user))
    return make_response_msg(status, msg)