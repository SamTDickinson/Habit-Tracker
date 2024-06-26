import os
from flask import Flask
from pymongo import MongoClient
from dotenv import load_dotenv, dotenv_values

from routes import pages

config = dotenv_values(".env")

load_dotenv()


def create_app():
    app = Flask(__name__)
    client = MongoClient(os.environ.get("MONGODB_URL"))
    app.db = client.get_default_database()
    app.register_blueprint(pages)
    return app
