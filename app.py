import datetime
from flask import Flask, render_template, request
from pymongo import MongoClient

def create_app():
    app = Flask(__name__)
    client = MongoClient("mongodb+srv://zhaoyufrank8825:yingying8825@cluster0.x1tdu.mongodb.net/test")
    app.db = client.myblog

    @app.route('/', methods=["GET", "POST"])
    def home():
        if request.method == "POST":
            entry = request.form.get("content")
            date = datetime.datetime.today().strftime("%Y-%m-%d")
            app.db.entries.insert({"content":entry, "date":date})
        entries_date = [
            (   
                entry["content"],
                entry["date"],
                datetime.datetime.strptime(entry["date"], "%Y-%m-%d").strftime("%b %d")
            )
            for entry in app.db.entries.find({})
        ]
        return render_template("home.html", entries=entries_date)
    return app
