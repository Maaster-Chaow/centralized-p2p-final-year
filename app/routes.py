from flask import request
from flask import jsonify

from app import app

APP_USER_AGENT = 'PocoPono'

def check_user_agent(handler):
    def check():
        #if str(request.user_agent) != "PocoPono":
        #    return "",401
        return handler()
    return check

@app.route('/', methods=["GET"])
@check_user_agent
def index():
    return "HELLO",200
