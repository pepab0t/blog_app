from . import db

from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin): # type: ignore
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())

    posts = db.relationship("Post", backref="user", cascade="all, delete")#, passive_deletes=True)
    comments = db.relationship("Comment", backref="user", cascade= "all, delete")#, passive_deletes=True)
    likes = db.relationship("Like", backref="user", cascade="delete, all")

    def __repr__(self) -> str:
        return f"User: {self.id}, Username: {self.username}"

class Post(db.Model): # type: ignore    
    __tablename__ = "post"

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False) # CASCADE ... delete user's posts when user is deleted

    comments = db.relationship("Comment", backref="post", cascade="all, delete")#), passive_deletes=True)
    likes = db.relationship("Like", backref="post", cascade="delete, all")

class Comment(db.Model): # type:ignore
    __tablename__ = "comment"

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"), nullable=False)

class Like(db.Model): # type:ignore
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"), nullable=False)

    