from app import app
from flask import request
from flask import jsonify, make_response

APP_USER_AGENT = 'PocoPono'

def check_user_agent(handler):
    def check():
        #if str(request.user_agent) != "PocoPono":
        #    return "",401
        #return handler()
        user_info = app.cache.get(request.remote_addr)
        if user_info:
            print('Host %s is list on port %s' %(user_info['ip'],
                                                      user_info['port']))
        return handler()
    return check

@app.route('/', methods=["GET"])
@check_user_agent
def index():
    print(request.user_agent)
    user_info = {
        'ip': request.remote_addr,
        'port': request.environ.get('REMOTE_PORT')
    }
    return jsonify(user_info), 200

@app.route('/', methods=['POST'])
def get_host_info():
    port = request.form.get('port')
    host = request.remote_addr
    host_entered = app.cache.set(host, port)
    peers = request.form.get('peers')
    if peers is None or len(peers) == 0:
        return ("OK", 200) if host_entered else ("Server Error", 500)
    else:
        peers = [ip.strip() for ip in peers.split(',')]
        live_hosts = {ip:app.cache.get(ip) for ip in peers}
        if live_hosts is None:
            return "OK", 200
        else:
            return jsonify(live_hosts), 200
