from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint, jsonify)
from flask_login import current_user, login_required
from flaskapp import db
from flaskapp.models import Post
from flaskapp.posts.forms import PostForm

import json

posts = Blueprint('posts', __name__)


@posts.route("/post/test", methods=['POST','GET'])
def test():
    s = 'Hi! I am your server here.'
    d = {}
    d['key1'] = s
    d['key2'] = None
    d['key3'] = None
    try:
        v = request.data.decode('utf-8')
        e = None
        d = json.loads(v)
        d['key1'] = s
    except Exception as err:
        e = "No data found"
        d['key1'] = s

    r = {
        "key1": d['key1'],
        "key2": d['key2'],
        "key3": d['key3'],
        "error": e
    }
    # Sample data returned example if no error
    # {
    #     "error": null,
    #     "key1": "Hi! I am your server here.",
    #     "key2": 128.0123,
    #     "key3": true
    # }
    return jsonify(r)
@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')


@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))
