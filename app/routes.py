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
            print('Earlier port number of %s is %s' %(user_info['ip'],
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
    app.cache.set(request.remote_addr, user_info)
    return jsonify(user_info), 200
