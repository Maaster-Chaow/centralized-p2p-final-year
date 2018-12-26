from flask import request
from flask import jsonify

from app import app

APP_USER_AGENT = 'PocoPono'


@app.route('/', methods=["GET"])
def index():
    return "HELLO",200
