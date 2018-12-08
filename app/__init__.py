import os, sys
sys.path.append(os.path.dirname(os.path.join('..', 'lib')))

from lib import CustomFlask, HostCache

app = CustomFlask(__name__)
app.cache = HostCache()

from app import routes
