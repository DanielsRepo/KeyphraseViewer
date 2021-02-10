import os

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv


load_dotenv()

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app.config["DEBUG"] = os.environ["DEBUG"]
    app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(os.path.abspath(os.path.dirname(__file__)), "app.db")

    user = os.environ["POSTGRES_USER"]
    pwd = os.environ["POSTGRES_PASSWORD"]
    host = os.environ["POSTGRES_HOST"]
    port = os.environ["POSTGRES_PORT"]
    db_name = os.environ["POSTGRES_DB"]

    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = f"postgresql+psycopg2://{user}:{pwd}@{host}:{port}/{db_name}"

    from .models import Text, Keyphrase

    db.init_app(app)
    with app.app_context():
        db.create_all()

    migrate = Migrate(app, db)

    from .routes import viewer_blueprint

    app.register_blueprint(viewer_blueprint)

    return app
