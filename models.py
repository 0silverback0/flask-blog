"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)
    
#get todays date
today = datetime.now()
today = today.strftime("%B %d, %Y %H:%M:%S")


#models
class User(db.Model):
    __tablename__ = 'users'

    def __repr__(self):
        u = self
        return f'<ID: {u.id}, first_name: {u.first_name}, last_name: {u.last_name}, img_url: {u.img_url}>'

    id = db.Column(db.Integer,
        primary_key=True,
        autoincrement=True)

    first_name = db.Column(db.String(50),
        nullable=False,
        unique=True)

    last_name = db.Column(db.String(50),
        nullable=False,
        unique=True)

    img_url = db.Column(db.String(), nullable=False, default='https://bit.ly/3tQncTZ')

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    
class Post(db.Model):
    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(150), nullable=False)
    created_at = db.Column(db.String(), default=today)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('User', backref='post')
    tags = db.relationship('Tags', secondary='post_tag', backref='post')

    def __repr__(self):
        p = self
        return f'<ID: {self.id} title: {self.title} content: {self.content} created_at: {self.created_at} user_id: {self.user_id}>'

    def get_all_post(user_id):
        posts = Post.query.filter(Post.user_id == user_id).all()
        return posts

class Tags(db.Model):
    """tags table"""
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True)

class PostTag(db.Model):
    """post tag table"""
    __tablename__ = 'post_tag'

    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), primary_key=True, nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True, nullable=False)

    tags = db.relationship('Tags', backref='posts')    
