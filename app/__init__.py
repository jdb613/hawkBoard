import os
from flask import Flask, request, current_app
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    """Construct the core application."""
    app = Flask(__name__)

    app.config.from_object(config_class)
    db.init_app(app)
    migrate.init_app(app, db)
    with app.app_context():

        # Import main Blueprint
        from app.main import bp as main_bp
        app.register_blueprint(main_bp)

        # Create tables for our models
        db.create_all()

        # Import Dash application
        from app.dash_application.dash_example import Add_Dash
        app = Add_Dash(app)

        # Compile assets
        # from application.assets import compile_assets
        # compile_assets(app)

        return app

from app import models
