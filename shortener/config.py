"""
link-shortener Flask config
"""
import os
from os.path import abspath, dirname

from dotenv import load_dotenv
from shortener import logger

# Get path of parent directory
basedir = abspath(dirname(dirname(__file__)))


def create_db(app):
    from shortener.models import db

    db.init_app(app)
    app.db = db
    return app.db


# pylint: disable=unused-variable
def init_logging(app):
    """
    Set up custom request logging

    Args:
        app: Flask application object
    """
    from flask import g, request
    from datetime import datetime

    @app.before_request
    def start_timer():
        g.start = datetime.utcnow().timestamp()

    @app.after_request
    def log_request(response):
        import colors

        now = datetime.utcnow().timestamp()
        duration = round(now - g.start, 3)
        timestamp = datetime.fromtimestamp(now).strftime('%Y/%m/%d %H:%M:%S')

        _ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        args = dict(request.args)

        log_params = [
            (_ip, 'red'),
            (timestamp, 'magenta'),
            (request.method, 'blue'),
            (request.path, 'yellow'),
            (args or '-', 'blue'),
            (response.status_code, 'white'),
            (duration, 'green'),
        ]
        parts = []
        for value, color in log_params:
            part = colors.color(f'{value}', fg=color)
            parts.append(part)
        line = ' '.join(parts)

        logger.info(line)
        return response


def load_config(app):
    """
    Load configuration for the app from environment variables and .env file

    Args:
        app: A Flask application
    """
    load_dotenv(dotenv_path='.env')

    db = os.getenv('db_name')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SERVER_NAME'] = os.environ.get('FLASK_SERVER_NAME', False)
    app.config['server_protocol'] = os.environ.get('server_protocol', '')
    app.config['access_token'] = os.environ.get('access_token', None)

    @app.after_request
    def add_header(response):
        response.cache_control.max_age = 0
        response.cache_control.no_cache = True
        response.cache_control.no_store = True
        response.cache_control.must_revalidate = True
        return response

    app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'development_key')
