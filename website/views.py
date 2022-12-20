
from flask import Blueprint, render_template, request, redirect, flash, url_for, jsonify
from flask_login import login_required, current_user
from .models import Post, User, Comment, Like
from . import db

views = Blueprint("views", __name__)

@views.route("/")
@views.route("/home")
@login_required
def index():
    posts: list[Post] = Post.query.all()
    return render_template("home.html", name=current_user.username, posts=posts) # type: ignore

@views.route("/new_post", methods=["GET", "POST"])
@login_required
def new_post():
    if request.method == "POST":
        post_text = request.form.get("text")

        assert post_text is not None, "Not defined html name `text`"

        if len(post_text) < 1:
            flash("Post cannot be empty.", category="error")
        else:
            post = Post(text=post_text, user_id=current_user.id) # type: ignore
            db.session.add(post)
            db.session.commit()
            flash("Post created!", category="success")

            return redirect(url_for("views.index"))

    return render_template("create_post.html")

@views.route("/delete_post/<int:id>")
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first()

    if post is None:
        flash("Post does not exist", category="error")
    elif post.user_id != current_user.id: # type: ignore
        flash("You do not have permissions to delete this post", category="error")
    else:
        db.session.delete(post)
        db.session.commit()
        flash("Post deleted", category="success")

    return redirect(url_for("views.index"))

@views.route("/posts/<username>")
@login_required
def posts(username: str):
    user = User.query.filter_by(username=username).first()

    # check if user exists
    if user is None:
        flash(f"User {username} does not exist", category="error")
        return redirect(url_for("views.index"))

    posts = user.posts

    return render_template("posts.html", posts=posts, username=username)

@views.route("/new_comment/<int:post_id>", methods=["POST"])
@login_required
def new_comment(post_id):

    text = request.form.get("text")

    assert text is not None, "Undefined `text`"

    if len(text) < 1:
        flash("Comment cannot be empty", category="error")
    else:
        post = Post.query.get(post_id)
        if post is not None:
            comment = Comment(text=text, user_id=current_user.id, post_id=post_id) # type: ignore
            db.session.add(comment)
            db.session.commit()
        else:
            flash("Post does not exist", category="error")

    return redirect(url_for("views.index"))
    
@views.route("/delete_comment/<int:id>")
@login_required
def delete_comment(id: int):
    comment: Comment = Comment.query.get(id)

    if comment is None:
        flash("Comment does not exist", category="error")
    elif current_user.id != comment.user_id and current_user.id != comment.post.user_id: # type: ignore
        flash("You don't have permissions to delete comment", category="error")
    else:
        db.session.delete(comment)
        db.session.commit()

    return redirect(url_for("views.index"))


@views.route("/like/<int:post_id>", methods=["POST"])
@login_required
def like(post_id: int):
    post = Post.query.get(post_id)
    like = Like.query.filter_by(user_id=current_user.id, post_id=post_id).first() # type: ignore

    if post is None:
        return jsonify({"error": "post does not exist"}, 400)
    elif like is not None:
        db.session.delete(like)
        db.session.commit()
    else:
        like = Like(user_id=current_user.id, post_id=post_id) # type:ignore
        db.session.add(like)
        db.session.commit()


    return jsonify({"likes": len(post.likes), "liked": current_user.id in map(lambda x: x.user_id, post.likes)}) # type: ignore
