import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Phone(db.Model):
    __tablename__ = "phones"
    asin = db.Column(db.String, primary_key=True)
    brand = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    url = db.Column(db.String)
    image = db.Column(db.String,)
    rating = db.Column(db.Numeric)
    totalReviews = db.Column(db.Integer)
    prices = db.Column(db.Numeric)
    grade = db.Column(db.String)

class User(db.Model):
    __tablename__ = "users"
    name = db.Column(db.String, primary_key=True)
    password = db.Column(db.String, nullable=False)

class Review(db.Model):
    __tablename__ = "reviews"
    ID = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, db.ForeignKey("users.name"), nullable=False)
    asin = db.Column(db.String, db.ForeignKey("phones.asin"),nullable=False)
    mark = db.Column(db.Integer, nullable=False)
    text = db.Column(db.String)
