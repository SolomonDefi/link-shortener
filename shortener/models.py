"""
URL Shortener SQLAlchemy database models
"""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class URL(db.Model):
    """
    User address model
    """

    __tablename__ = 'urls'
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime)
    short = db.Column(db.String(32), index=True)
    target = db.Column(db.String(512))

    def __init__(self, **kwargs):
        created = kwargs.get('created')
        if created is None:
            kwargs['created'] = datetime.utcnow()
        super().__init__(**kwargs)

    def to_web(self, config):
        short_url = f'{config["server_protocol"]}{config["SERVER_NAME"]}/{self.short}'
        return {
            'id': self.id,
            'created': self.created.isoformat(),
            'short': self.short,
            'short_url': short_url,
            'target': self.target,
        }
