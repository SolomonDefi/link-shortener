"""
Entry point for uwsgi
"""

from application import create_app

application = create_app()

if __name__ == '__main__':
    application.run()
