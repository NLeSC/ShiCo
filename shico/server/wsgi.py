''' RUN:
$ gunicorn --bind 0.0.0.0:8000 --timeout 1200 shico.server.wsgi:app
'''

from shico.server.app import app
from shico.server.utils import initApp

from flask import current_app

from shico.server.config import files, binary, useMmap, w2vFormat, cleaningFunctionStr

with app.app_context():
    initApp(current_app, files, binary, useMmap,
            w2vFormat, cleaningFunctionStr)
