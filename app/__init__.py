
from flask import Flask  
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

#db is an instance of SQLAlchemy class.  this is how we interat with our database.
#these are in the global scope!
db = SQLAlchemy()
#migrate is saying how we configure the database.  how do we get to something (our database)
#with the relations we want.
migrate = Migrate()

def create_app():
    # __name__ stores the name of the module we're in
    app = Flask(__name__)
    #configuration is a dictionary: we're setting key-value pairs.
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    #if the below isn't working, change localhost to 127.0.0.1
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://postgres:postgres@localhost:5432/journals_development"

    #you have to import this before db.init_app(app)
    from app.models.journal import Journal

    #this is where we connect our database to our application.
    db.init_app(app)
    #migrate will generate ways to set up our database.
    migrate.init_app(app, db)

    #make sure Flask knows app functions exist
    from .routes.journal import journal_bp
    app.register_blueprint(journal_bp)

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://postgres:postgres@localhost:5432/bikes_development"

    from app.models.bike import Bike

    db.init_app(app)
    migrate.init_app(app, db)

    from .routes.bike import bike_bp
    app.register_blueprint(bike_bp)

    return app