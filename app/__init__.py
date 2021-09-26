from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_avatars import Avatars

app = Flask(__name__,
    static_folder="static/")
app.config.from_object('config')
avatars = Avatars(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import http_errors, views, models

