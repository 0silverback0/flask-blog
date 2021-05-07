"""Blogly application."""

from flask import Flask, request, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tags, PostTag, today


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "Alchemist"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/')
def home():
    users = User.query.all()
    return redirect('/users')

@app.route('/users')
def show_users():
    users = User.query.all()
    return render_template('index.html', users=users)

@app.route('/user/new')
def add_user():
    return render_template('add-user.html')

@app.route('/users/new', methods=['POST'])
def test():
    first = request.form["first"]
    last = request.form['last']
    url = request.form['img']
    url = url if url else None
    
    new_user = User(first_name=first, last_name= last, img_url=url)
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>')
def user_details(user_id):
    user = User.query.get_or_404(user_id)
    posts = Post.get_all_post(user_id)
    return render_template('details.html', user=user, posts=posts)

@app.route('/users/<int:user_id>/edit')
def edit_page(user_id):
    user = User.query.get(user_id)
    return render_template('edit.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def edited_user(user_id):
    user = User.query.get(user_id)
    user.first_name = user.first_name if request.form['first'] == '' else request.form['first']
    user.last_name = user.last_name if request.form['last'] == '' else request.form['last']
    user.img_url = user.img_url if request.form['img'] == '' else request.form['img']

    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>/delete')
def delete_user(user_id):
    User.query.filter_by(id=user_id).delete()
    db.session.commit()
    return redirect('/users')

@app.route('/users/<int:user_id>/post/new')
def new_post(user_id):
    user = User.query.get(user_id)
    return render_template('newpost.html', user=user)

@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def add_new_post(user_id):
    user_id = user_id
    title = request.form["title"]
    content = request.form['content']

    new_post = Post(title=title, content=content, user_id=user_id)

    db.session.add(new_post)
    db.session.commit()
    
    return redirect(f'/users/{user_id}')

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    post = Post.query.get(post_id)
    return render_template('post.html', post=post)

@app.route('/posts/<int:post_id>/edit')
def edit_post(post_id):
    post = Post.query.get(post_id)
   
    return render_template('edit-post.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def edited_post(post_id):
    post_id = post_id
    post = Post.query.get(post_id)
    post.title = post.title if request.form['title']  == '' else request.form['title']
    post.content = post.content if request.form['content'] == '' else request.form['content']

    db.session.commit()

    return redirect(f'/posts/{post_id}')

@app.route('/posts/<int:post_id>/delete')
def delete_post(post_id):
    Post.query.filter_by(id=post_id).delete()
    db.session.commit()
    return redirect('/users')

@app.route('/tags')
def tag_list():
    tags = Tags.query.all()

    return render_template('tag-list.html', tags=tags)