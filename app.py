from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import os

from dags.spotify_etl import run_spotify_etl

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import *

@app.route("/")
def home():
    run_spotify_etl()
    return "spotify history app"

if __name__ == '__main__':
    app.run()
