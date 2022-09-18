from flask import Blueprint

users = Blueprint('users', __name__)

@users.route("/login", methods=['GET', 'POST'])
def login():

    return "Here is login page"

@users.route("/user/<string:username>")
def user_posts(username):

    return "username is " + username