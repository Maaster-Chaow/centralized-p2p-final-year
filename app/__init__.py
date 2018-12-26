"""Package containing server logic

./lib: contains usefull local libraries.
./instance: configurations.
"""

import os

from flask_api import FlaskAPI
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate

#from app.lib import CustomFlask, HostCache
from app.instance.config import app_config
#from app.models import Users


app = FlaskAPI(__name__, instance_relative_config=True)
app.config.from_object(app_config[os.getenv('SERVER_ENV')])
#app.config.from_pyfile('config.py')
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#DB = SQLAlchemy(app)
#migrate = Migrate(app, DB)

from app import routes #models
