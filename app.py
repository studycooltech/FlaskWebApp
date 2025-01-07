from flask import Flask
from config import Config
from extensions import db, migrate  # Import migrate
from flask_migrate import Migrate
from blueprints.user.models import User


#Insert into database some initial data
def insert_initial_data():
    # Insert some initial data if no users exist
    if User.query.count() == 0:
        user1 = User(name="Shyam", email="shyam@example.com")
        user2 = User(name="Mohit", email="mohit@example.com")
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)  # Initialize Migrate



    # Register blueprints
    from blueprints.user.routes import user_bp
    app.register_blueprint(user_bp, url_prefix='/api/users')

    from blueprints.home.routes import home_bp
    app.register_blueprint(home_bp,url_prefix='/')  # No prefix for the home blueprint


    # Call insert_initial_data function to add initial data to the database
    with app.app_context():
        insert_initial_data()  # Ensure this is run within an app context

    return app
