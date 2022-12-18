from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from .models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    print(current_user)
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        assert email is not None, "No input email"
        assert password is not None, "No input password"

        user = User.query.filter_by(email=email).first()
        if user is not None:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                flash("Logged in!", category="success")
                return redirect(url_for("views.index"))
            else:
                flash("Password is incorrect", category="error")
        else:
            flash("Email does not exist", category="error")

    return render_template("login.html")

@auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        email = request.form.get("email")
        username = request.form.get("username")
        password1 = request.form.get("password")
        password2 = request.form.get("confirm_password")

        assert email is not None, "No input email"
        assert username is not None, "No input username"
        assert password1 is not None, "No input password"
        assert password2 is not None, "No input confirm_password"

        email_exists = User.query.filter_by(email=email).first() is not None
        username_exists = User.query.filter_by(username=username).first() is not None

        if email_exists:
            flash("Email is already taken", category="error")
        elif username_exists:
            flash("Username is already taken", category="error")
        elif password1 != password2:
            flash("Passwords don't match", category="error")
        elif len(username) < 2:
            flash("Username too short (min 2 characters)", category="error")
        elif len(password1) < 6:
            flash("Password too short (min 6 characters)", category="error")
        else:
            new_user = User(email=email, username=username, password=generate_password_hash(password1, method="sha256"))
            db.session.add(new_user)
            db.session.commit()
            flash("User created successfully", category="success")

            # autologin after sign up
            login_user(new_user, remember=True)
            
            return redirect(url_for("views.index"))
    return render_template("signup.html")

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.index"))