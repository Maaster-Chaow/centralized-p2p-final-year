from app import app
from flask import request
from flask import jsonify

@app.route('/', methods=["GET"])
def index():
    return jsonify({
        'ip': request.remote_addr,
        'port': request.environ.get('REMOTE_PORT')
    }), 200
