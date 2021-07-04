from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)
mongo = PyMongo(app, uri="mongodb://localhost:27017/mission_to_mars")


@app.route("/")
def echo():
    final_mars_data = mongo.db.collection.find_one()
    return render_template("index.html", final_mars_data=final_mars_data)


@app.route("/scrape")
def scrapping_mars():
    final_mars_data = scrape_mars.scrape()
    mongo.db.collection.update({}, final_mars_data, upsert=True)

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
