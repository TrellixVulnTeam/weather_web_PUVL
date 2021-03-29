import base64
import os

from . import db
from flask_login import UserMixin, current_user


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.Integer)
    name = db.Column(db.String(50))
    password = db.Column(db.String(50))
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)

    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'password': self.password,
            'token': self.token
        }
        return data

    def from_dict(self, data, new_user=False):
        for field in ['name', 'password', 'token']:
            if field in data:
                setattr(self, field, data[field])

    def get_token(self):
        user_token = self.token
        if user_token is None:
            self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
            db.session.add(self)
            db.session.commit()
            return self.token
        else:
            return user_token


class Item(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    text = db.Column(db.String(1000))
    token = db.Column(db.String(32), index=True)

    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'text': self.text
        }
        return data
