from flask import Response, jsonify


class JSONResponse(Response):
    '''Custom Response class'''
    default_mimetype = 'application/json'
    
    @classmethod
    def force_type(cls, response, environ=None):
        response = jsonify(response)
        return super(JSONResponse, cls).force_type(response, environ=environ)
        