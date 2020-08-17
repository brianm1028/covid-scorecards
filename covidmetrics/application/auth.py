"""Routes for user authentication."""
from flask import Blueprint, redirect, render_template, flash, request, session, url_for
from flask_login import login_required, logout_user, current_user, login_user
from .forms import LoginForm, SignupForm
from .models import User
from . import login_manager
from . import db


# Blueprint Configuration
auth_bp = Blueprint(
    'auth_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in on every page load."""
    if user_id is not None:
        return User.query.get(user_id)
    return None


@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash('You must be logged in to view that page.')
    return redirect(url_for('auth_bp.login_form'))

@auth_bp.route('/login', methods=['GET'])
def login_form():
    return render_template('login.html')

@auth_bp.route('/login', methods=['POST'])
def login_post():
    if current_user.is_authenticated:
        return redirect(url_for('main_bp.profile'))

    form = LoginForm()
    remember = True if form.remember.data else False

    user = User.query.filter_by(email=form.email.data).first()
    if user and user.check_password(password=form.password.data):
        login_user(user, remember=remember)
        next_page = request.args.get('next')
        return redirect(next_page or url_for('main_bp.profile'))
    flash('Invalid username/password combination')
    return redirect(url_for('auth_bp.login_form'))

@auth_bp.route('/signup', methods=['GET'])
def signup_form():
    return render_template('signup.html')

@auth_bp.route('/signup', methods=['POST'])
def signup_post():
    form = SignupForm()
    existing_user = User.query.filter_by(email=form.email.data).first()
    if existing_user is None:
        user = User(
            name=form.name.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()  # Create new user
        login_user(user)  # Log in as newly created user
        return redirect(url_for('main_bp.index'))
    flash('A user already exists with that email address.')

@auth_bp.route("/logout")
@login_required
def logout():
    """User log-out logic."""
    logout_user()
    return redirect(url_for('auth_bp.login_form'))