import os
import random
import string
from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from time import time
import jwt
import hashlib

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from app import db, login


class User(UserMixin,db.Model):
    __tablename__ = 'Users'
    __table_args__ = {"schema":"system", 'extend_existing': True }



    UserId = db.Column(db.Integer, primary_key=True)
    Role = db.Column(db.String(64))
    FirstName = db.Column(db.String(64))
    LastName = db.Column(db.String(64))
    UserName = db.Column(db.String(64), index=True, unique=True)
    PasswordHash = db.Column(db.String(128))
    PasswordSalt = db.Column(db.String(16))
    TokenId = db.Column(db.String(128))

    def get_id(self):
           return (self.UserId)

    def set_password(self, password):
        self.PasswordHash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.PasswordHash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

    def __repr__(self):
        return '<User {}>'.format(self.UserName)  

@login.user_loader
def load_user(UserId):
    return User.query.get(int(UserId))