import os
import requests

from flask import Flask, render_template, jsonify, request
from models import *
from flask import session
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_sqlalchemy import *
from sqlalchemy import and_, or_
from flask_socketio import SocketIO, emit


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    counter = User.query.filter(and_(User.name==username, User.password==password)).count()

    if counter == 1:
        session['username'] = username
        return render_template("search.html")

    else:
        return render_template("error.html", message="Username or password is wrong")

@app.route("/register", methods=["GET","POST"])
def register():
    return render_template("register.html")

@app.route("/store", methods=["POST"])
def store():
    username = request.form.get("username")
    password = request.form.get("password")
    count = User.query.filter(User.name==username).count()

    if count > 0:
        return render_template("error.html",message="Username exists, please choose another name.")
    else:
        user = User(name=username, password=password)
        db.add(user)
        db.commit()
        return render_template("index.html",message="注册成功")

@app.route("/search", methods=["POST"])
def search():
    asin = request.form.get("asin")
    brand = request.form.get("brand")
    title = request.form.get("title")
    grade = request.form.get("grade")
    order = request.form.get("order")

    per="%"
    counter = Phone.query.filter(and_(Phone.asin.like(per+asin+per),Phone.brand.like(per+brand+per),Phone.title.like(per+title+per),Phone.grade.like(per+grade+per))).count()

    if counter > 0:
        
        if order =='A':
            phones = Phone.query.filter(and_(Phone.asin.like(per+asin+per),Phone.brand.like(per+brand+per),Phone.title.like(per+title+per),Phone.grade.like(per+grade+per))).all()
            return render_template("phones.html", phones=phones)
            
        elif order =='B':
            phones = Phone.query.order_by(Phone.rating.desc()).filter(and_(Phone.asin.like(per+asin+per),Phone.brand.like(per+brand+per),Phone.title.like(per+title+per),Phone.grade.like(per+grade+per))).all()
            return render_template("phones.html", phones=phones)
            
        elif order =='C':
            phones = Phone.query.order_by(Phone.prices.desc()).filter(and_(Phone.asin.like(per+asin+per),Phone.brand.like(per+brand+per),Phone.title.like(per+title+per),Phone.grade.like(per+grade+per))).all()
            return render_template("phones.html", phones=phones)
            
        else:
            phones = Phone.query.order_by(Phone.prices).filter(and_(Phone.asin.like(per+asin+per),Phone.brand.like(per+brand+per),Phone.title.like(per+title+per),Phone.grade.like(per+grade+per))).all()
            return render_template("phones.html", phones=phones)
    else:
        return render_template("error.html", message="No such phone")

@app.route("/phones/<asin>")
def phone(asin):

    phone = Phone.query.get(asin)
    if phone is None:
        return render_template("error.html", message="No such phone")
    else:
        reviews = Review.query.filter(Review.asin==asin).all()
        counter = Review.query.filter(and_(Review.asin==asin),(Review.username==session['username'])).count()
        return render_template("phone.html", phone=phone, remarks=reviews,counter=counter)

@app.route("/comment/<asin>", methods=["POST"])
def comment(asin):
        # Get form information.
        username = session['username']
        mark = request.form.get("mark")
        text = request.form.get("text")
        ID = Review.query.count()+1
        
        review = Review(ID = ID,username=username, asin=asin, mark=mark, text=text)
        db.add(review)
        db.commit()
        phone = Phone.query.get(asin)
        reviews = Review.query.filter(Review.asin==asin).all()
        counter = Review.query.filter(and_(Review.asin==asin),(Review.username==session['username'])).count()
        return render_template("phone.html", phone=phone, remarks=reviews,counter=counter)

@app.route("/logout", methods=["POST"])
def logout():
    session.pop('username',None)
    return render_template("index.html")

if __name__ == "__main__":
    app.run()