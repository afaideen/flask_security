import sys

import requests
from flask import session, render_template, url_for, flash, redirect, request, abort, Blueprint, jsonify, Response, make_response
from flask_login import current_user, login_required
from flaskapp import db, cache, app
# from flaskapp import socketio
from flaskapp.example1.routes import example1
from flaskapp.example1.utils import get_ip
from flaskapp.models import Post
from flaskapp.posts.forms import PostForm


import json

posts = Blueprint('posts', __name__)

# @socketio.on('my event')
# def handle_my_custom_event(json):
#     print('received json: ' + str(json))


# Sample data returned example if no error
# {
#     "error": null,
#     "key1": "Hi! I am your server here.",
#     "key2": 128.0123,
#     "key3": true
# }
@posts.route("/post/test", methods=['POST','GET'])
# @login_required
def test():
    s = 'Hi! I am your server here.'
    d = {}
    d['key1'] = s
    d['key2'] = None
    d['key3'] = None
    # session_param1 = session.get("session_param1")
    # print("session_param1 is %s" %(session_param1))
    cache_param1 = cache.get("cache_param1")
    print("cache_param1 is %s" % (cache_param1))
    cache.delete("cache_param1")
    try:
        v = request.data.decode('utf-8')
        e = None
        d = json.loads(v)
        print("client: ", d)
        d['key1'] = s
        print("server: ", d)
    except Exception as err:
        e = "No data found"
        d['key1'] = s
        print(e)
    r = {
        "key1": d['key1'],
        "key2": d['key2'],
        "key3": d['key3'],
        "error": e
    }

    return jsonify(r)

@posts.route("/test_berkeley", methods=['POST'])
@login_required
def test_berkeley():
    # session["session_param1"] = "msg123"
    cache.set("cache_param1", "msg123")
    try:
        v = request.data.decode('utf-8')
        e = None
        d = json.loads(v)
        print("client: ", d)
        host = d['host']
    except Exception as err:
        e = "error in data format"
        print(e)
        d = {}
        d['host'] = None
        d['error'] = e
        return jsonify(d)

    if sys.platform == 'win32':
        ip_address = request.remote_addr
        remote_port = request.environ.get('REMOTE_PORT')
    else:
        ip_address_ = request.environ['HTTP_X_FORWARDED_FOR'].split(",")
        ip_address = ip_address_[0]
        remote_port = request.headers.get('REMOTE_PORT')
    print("ip_address: " + ip_address)
    print("remote_port: " + str(remote_port))

    url = "http://%s" %(host)
    json_body_data = {
        "msg": "hello there!",
        "ipaddr": get_ip()    ,
    }

    e = 1
    try:
        if sys.platform == 'win32':
            r = requests.post(url, json = json_body_data, timeout = 1)
        else:
            r = requests.post(url, json = json_body_data, timeout = 5)
        print(r.text)
    except Exception as err:
        e = "Can't find board"
        print(e)
        d = {}
        d['host'] = None
        d['error'] = e
        return jsonify(d)


    return jsonify(r.json())

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
