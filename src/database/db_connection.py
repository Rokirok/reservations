from os import getenv
from app import app
from flask_sqlalchemy import SQLAlchemy

app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URI").replace("://", "ql://", 1)
db = SQLAlchemy(app)
