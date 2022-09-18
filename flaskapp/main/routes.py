from flask import render_template, request, Blueprint


main = Blueprint('main', __name__)



@main.route("/")
@main.route("/index")
def about():
    return "Hi there!"
