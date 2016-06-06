from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Example(db.Model):
    __tablename__ = 'examples'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
