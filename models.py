from flask import *
from . import db
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, ForeignKey, Date

class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    firstname=db.Column(db.String(150))
    password=db.Column(db.String(150))
    username=db.Column(db.String(150))
    email=db.Column(db.String(150))
    image=db.relationship("Image")
class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.Text, unique=True, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text, nullable=False)
    likes=db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
