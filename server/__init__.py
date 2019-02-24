import os

from flask import Flask
from werkzeug.utils import redirect




def create_app(config=None):
    from .config import app_config
    from .customs import JSONResponse
    
    flask_env = os.getenv('FLASK_ENV', 'production')
    app = Flask(__name__)
    app.config.from_object(app_config[flask_env])
    app.response_class = JSONResponse
    if not config is None:
        app.config.from_object(app_config[config])
    
    with app.app_context():
        from .customs import pending_regs
        from .models import db, migrate, User
        from .mail import mail
        
        db.init_app(app)
        mail.init_app(app)
        migrate.init_app(app, db)
        pending_regs.init_app(app)
        
        @app.shell_context_processor
        def make_shell_context():
            return dict(db=db, User=User)
        
        @app.before_request
        def force_secure():
            from flask import request
            if app.config.get('SSL'):
                if request.endpoint in app.view_functions and \
                    not request.is_secure:
                    return redirect(request.url.replace('http://', 'https://'))
        
        from . import registration
        app.register_blueprint(registration.bp)
        
        return app