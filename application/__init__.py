"""Initialize app."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    """Construct the core application."""
    app = Flask(__name__,
                instance_relative_config=False)
    db.init_app(app)
    app.config.from_object('config.Config')

    with app.app_context():

        # Import main Blueprint
        from application import routes
        app.register_blueprint(routes.main_bp)

        # Create tables for our models
        db.create_all()

        # Import Dash application
        from application.dash_application.dash_example import Add_Dash
        app = Add_Dash(app)

        # Compile assets
        from application.assets import compile_assets
        compile_assets(app)

        return app
