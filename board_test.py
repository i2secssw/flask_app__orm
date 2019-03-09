# -- coding: utf-8 --

from flask import Flask, g, redirect, render_template, request, url_for, session
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import pbkdf2_sha256
import time, datetime, sqlite3

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/board.db'
app.secret_key = 'key'
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    idx = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    mobile = db.Column(db.String(14), unique=True)

    def __init__(self, user_id, password, name, email, mobile):
        self.user_id = user_id
        hash_password = pbkdf2_sha256.hash(password)
        self.password = hash_password
        self.name = name
        self.email = email
        self.mobile = mobile

    def verify_login(self, _password):
        return pbkdf2_sha256.verify(_password, self.password)

    def __repr__(self):
        return 'User %r' % self.user_id

def user_add(user_id, password, name, email, mobile):
    _user = User(user_id, password, name, email, mobile)
    db.session.add(_user)
    db.session.commit()

def user_update(user_id, password, name, email, mobile):
    _user = User.query.filter(User.user_id == user_id).first()
    _user.email = email if email else _user.email
    _user.name = name if name else _user.name
    _user.mobile = mobile if mobile else _user.mobile
    _user.password = pbkdf2_sha256.hash(password) if password else _user.password
    db.session.add(_user)
    db.session.commit()

def user_delete(user_id):
    _user = User.query.filter(User.user_id == user_id).first()
    db.session.delete(_user)
    db.commit()

def get_user(user_id):
    _users = db.session.query(User).filter_by(user_id=user_id).first()
    return _users

class Board(db.Model):
    __tablename__ = 'board'
    idx = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    writer = db.Column(db.String(30), nullable=False)
    ctime = db.Column(db.String(30))

    def __init__(self, title, content, writer, ctime):
        self.title = title
        self.content = content
        self.writer = writer
        self.ctime = ctime
    
def write_post(title, content, writer, ctime):
    _bpost = Board(title, content, writer, ctime)
    db.session.add(_bpost)
    db.session.commit()

def delete_post(idx):
    _bpost = Board.query.filter(Board.idx == idx).first()
    db.session.delete(_bpost)
    db.session.commit()
    
def modify_post(idx, title, content):
    _bpost = Board.query.filter(Board.idx == idx).first()
    _bpost.title = title if title else _bpost.title
    _bpost.content = content if content else _bpost.password
    db.session.add(_bpost)
    db.session.commit()

def get_post(idx):
    _bpost = db.session.query(Board).filter_by(idx=idx).first()
    return _bpost

def post_list():
    _bpost = []
    for row in db.session.query(Board).all():
        _bpost.append((row.idx,row.title,row.content,row.writer,row.ctime))
    return _bpost

if __name__ == "__main__":
    pass
