from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'Secret'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://database_12om_user:WuFSYuH5L5B4NTbHOPd3xjERqaxHcyCA@dpg-cppe3vij1k6c73ehhmog-a.frankfurt-postgres.render.com/database_12om'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        # Ensure all models are imported and registered here
        from .models import User, Post, Like  # Import all models

        # Create tables based on models
        db.create_all()

        # Print a message for debugging purposes
        print("All tables created successfully.")

    # Import views and auth blueprints
    from .views import views
    from .auth import auth

    # Register blueprints
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # Define user loader function
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app
