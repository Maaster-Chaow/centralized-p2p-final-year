from flask import Response, jsonify, current_app
from cacheout import Cache

from .config import OTP_TIME_OUT


def make_response_msg(status, msg, **kwargs):
    resp = dict(status=status, msg=msg)
    for name,value in kwargs.items():
        resp[name] = value
    return resp


class JSONResponse(Response):
    '''Custom Response class'''
    default_mimetype = 'application/json'
    
    @classmethod
    def force_type(cls, response, environ=None):
        response = jsonify(response)
        return super(JSONResponse, cls).force_type(response, environ=environ)


class RegisCache:
    def init_app(self, app):
        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions.setdefault('reg_pending', {})
        app.extensions['reg_pending'][self] = Cache(ttl=OTP_TIME_OUT)
        self.app = app
    
    @property
    def reg_pending(self):
        app = current_app or self.app
        return app.extensions['reg_pending'][self]
    
    @property
    def ttl(self):
        return self.reg_pending.ttl
    
    def get(self, key, default=None):
        return self.reg_pending.get(key, default)
    
    def set(self, key, val, ttl=None):
        self.reg_pending.set(key, val, ttl)
    
    def clear(self):
        self.reg_pending.clear()
    
    def configure(self, maxsize=None, ttl=None, timer=None, default=None):
        self.reg_pending.configure(maxsize,ttl,timer,default)
    
    def copy(self):
        return self.reg_pending.copy()
    
    def delete(self, key):
        return self.reg_pending.delete(key)
    
    def delete_expired(self):
        return self.reg_pending.delete_expired()
    
    def delete_many(self, iteratee):
        return self.reg_pending.delete_many(iteratee)
    
    def evict(self):
        return self.reg_pending.evict()
    
    def expire_times(self):
        return self.reg_pending.expire_times()
    
    def expired(self, key, expires_on):
        return self.reg_pending.expired(key, expires_on)
    
    def full(self):
        return self.reg_pending.full()
    
    def has(self, key):
        return self.reg_pending.has(key)
    
    def items(self):
        return self.reg_pending.items()
    
    def keys(self):
        return self.reg_pending.keys()
    
    def popitem(self):
        return self.reg_pending.popitem()
    
    def size(self):
        return self.reg_pending.size()
    
    def values(self):
        return self.reg_pending.values()
    
    def __contains__(self, key):
        return key in self.reg_pending


pending_regs = RegisCache()