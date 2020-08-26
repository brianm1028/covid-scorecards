from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_caching import Cache
from flask_session import Session
from .Permissions import Permissions
from datetime import datetime

login_manager = LoginManager()
db = SQLAlchemy()
cache = Cache()
sess = Session()

def create_app():
    """Initialize the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')
    app.config['TEMPLATES_AUTO_RELOAD'] = True


    # Initialize Plugins
    db.init_app(app)
    login_manager.login_view = 'auth_bp.login'
    login_manager.init_app(app)

    cache.init_app(app)
    sess.init_app(app)

    @app.context_processor
    def inject_session():
        return dict(session=sess)

    @app.context_processor
    def inject_datetime():
        return dict(dnow=datetime.now())

    @app.context_processor
    def check_permissions():
        def check_perms(perm, permset):
            return Permissions.check(perm, permset)
        return dict(check_perms=check_perms)

    @app.context_processor
    def lookup_permissions():
        def lookup_perm(perm):
            return Permissions.lookup(perm)
        return dict(lookup_perm=lookup_perm)

    app.add_template_global(Permissions.lookups(), 'permissions')

    with app.app_context():
        # Include our Routes
        from .main import main_bp
        from .auth import auth_bp
        from .admin import admin_bp
        from .snapshots import snap_bp
        from .geo import geo_bp
        from .ppe import ppe_bp
        from .space import space_bp
        from .staff import staff_bp
        from .trans import trans_bp

        # Register Blueprints
        app.register_blueprint(main_bp)
        app.register_blueprint(auth_bp)
        app.register_blueprint(admin_bp)
        app.register_blueprint(snap_bp)
        app.register_blueprint(geo_bp)
        app.register_blueprint(ppe_bp)
        app.register_blueprint(space_bp)
        app.register_blueprint(staff_bp)
        app.register_blueprint(trans_bp)


        return app
