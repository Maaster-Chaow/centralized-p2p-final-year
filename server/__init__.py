import os

from flask import Flask, g




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
        
        from . import registration
        app.register_blueprint(registration.bp)
        
        return app