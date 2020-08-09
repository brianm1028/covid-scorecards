from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_caching import Cache

#login_manager = LoginManager()
#db = SQLAlchemy()
cache = Cache()


def create_app():
    """Initialize the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')
    app.config['TEMPLATES_AUTO_RELOAD'] = True

    # Initialize Plugins
    #db.init_app(app)
    #login_manager.init_app(app)

    cache.init_app(app)

    with app.app_context():
        # Include our Routes
        from . import main
        #from . import auth
        from . import snapshots

        # Register Blueprints
        app.register_blueprint(main.main_bp)
        #app.register_blueprint(auth.auth_bp)
        app.register_blueprint(snapshots.snap_bp)

        # Create Database Models
        #db.create_all()



        return app
