from flask import render_template, request, Blueprint

from flaskapp import login_manager
from flaskapp.models import Post

main = Blueprint('main', __name__)

@login_manager.user_loader
@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)

@main.route("/about")
def about():
    return "Hi there!"
