import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail

from server.config import app_config
from server.customs import JSONResponse


_flask_env = os.getenv('FLASK_ENV', 'production')
app = Flask(__name__.split('.')[0])
app.config.from_object(app_config[_flask_env])
app.response_class = JSONResponse
db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)


from server import routes
from server.models import User


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User)