from flask import Blueprint, render_template, url_for, redirect, flash
from flask_login import current_user

from flaskapp import bcrypt, db
from flaskapp.models import User
from flaskapp.users.form import RegistrationForm

users = Blueprint('users', __name__)


@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('users.login'))

    return render_template('register.html', title='Register', form=form)
@users.route("/login", methods=['GET', 'POST'])
def login():

    return "Here is login page"

@users.route("/user/<string:username>")
def user_posts(username):

    return "username is " + username