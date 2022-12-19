from flask import render_template, request, Blueprint

from flaskapp import cache
from flaskapp.models import Post

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, title="My Home Page")

@main.route("/about")
def about():
    return render_template('about.html', title='About')


# class MyObj:
#     pass
#
#
# a = MyObj()
# a.b = 1
# a.c = 'hello'
# a.d = True
#
# cache.set('a_myobj', a)
# my_a_obj = cache.get('a_myobj')
E = 1


