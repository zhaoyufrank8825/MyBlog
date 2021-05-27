import datetime, os
from flask import Flask, render_template, request
from pymongo import MongoClient
from dotenv import load_dotenv


load_dotenv()

def create_app():
    app = Flask(__name__)
    client = MongoClient(os.environ.get("MONGODB_URI"))
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
