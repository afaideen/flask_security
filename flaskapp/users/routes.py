from flask import Blueprint

from flaskapp.users.form import RegistrationForm

users = Blueprint('users', __name__)


@users.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    return None
@users.route("/login", methods=['GET', 'POST'])
def login():

    return "Here is login page"

@users.route("/user/<string:username>")
def user_posts(username):

    return "username is " + username