""" Main entry point to the link-shortener app

`create_app` builds the app and sets global variables necessary for uwsgi
"""
from flask import Flask
from shortener.config import load_config, create_db, init_logging
from shortener import logger


def create_app(config_override=None):
    """
    App factory function

    Args:
        config_override: Dictionary for overriding app config

    Returns:
        A Flask application object
    """
    app = Flask(__name__)

    load_config(app)
    if config_override:
        app.config.update(config_override)

    create_db(app)
    init_logging(app)

    from shortener import make_shortener

    app.register_blueprint(make_shortener(app))
    logger.info(f'Server name: {app.config.get("SERVER_NAME")}')
    return app


if __name__ == '__main__':
    from werkzeug.serving import WSGIRequestHandler

    class CustomRequestHandler(WSGIRequestHandler):

        # pylint: disable=redefined-builtin
        def log(self, type, message, *args):
            pass

        def log_request(self, code='-', size='-'):
            pass

    application = create_app()

    application.run(host='0.0.0.0', port=5050, request_handler=CustomRequestHandler)
