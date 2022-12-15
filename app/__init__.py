from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
from flask_cors import CORS
import os

db = SQLAlchemy()
migrate = Migrate()
load_dotenv()


def create_app(testing=None):
    # __name__ stores the name of the module we're in
    app = Flask(__name__)
    CORS(app)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config['CORS_HEADERS'] = 'Content-Type'
    if testing is None:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI")
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_TEST_DATABASE_URI")

    from app.models.bike import Bike

    db.init_app(app)
    migrate.init_app(app, db)

    from .routes.bike import bike_bp
    app.register_blueprint(bike_bp)

    from .routes.cyclist import cyclist_bp
    app.register_blueprint(cyclist_bp)

    return app