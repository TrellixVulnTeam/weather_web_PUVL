import base64
from datetime import datetime, timedelta
import os
import re

from . import db
from flask_login import UserMixin


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

    def from_dict(self, data):
        for field in ['name', 'password', 'token']:
            if field in data:
                setattr(self, field, data[field])

    def get_token(self):
        user_token = self.token
        now = datetime.now()
        if self.token is None or (self.token_expiration < now + timedelta(seconds=300)):
            items_token = Item.query.filter_by(token=self.token).all()
            for i in items_token:
                print(i.token)
            self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
            self.token_expiration = now + timedelta(seconds=3600)
            while len(re.findall('[/]+', self.token)) > 0:
                self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
            for item in items_token:
                item.token = self.token
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
