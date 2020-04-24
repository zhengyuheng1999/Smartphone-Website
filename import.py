import csv
import os

from flask import Flask, render_template, request
from models import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

def main():
    f = open("smartphone.csv")
    reader = csv.reader(f)
    for asin, brand, title, url, image, rating, reviewUrl, totalReviews, prices in reader:
        if asin !="":
            phone = Phone(asin=asin, brand=brand, title=title, url=url, image=image, rating=rating, reviewUrl=reviewUrl, totalReviews=totalReviews, prices=prices)
            db.session.add(phone)
        print(f"Added phone marked {asin}")
    db.session.commit()

if __name__ == "__main__":
    with app.app_context():
        main()
