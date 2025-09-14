from flask import Blueprint, request, render_template, redirect, url_for, flash, current_app, make_response
from utils import decodeToken, createToken, handleError
from db import getUser, getUserEmail, insertUser
from middleware.authMiddleware import login_required

userRouter = Blueprint("userRouter", __name__, url_prefix="/users")


@userRouter.route("/signup", methods=["GET", "POST"])
@handleError("Signup faild")
def signup():
    if request.method == "POST":
        userName = request.form.get("userName")
        email = request.form.get("email")
        password = request.form.get("password")
        bcrypt = current_app.extensions["bcrypt"]
        passwordHash = bcrypt.generate_password_hash(password).decode('utf-8')
        insertUser(userName, email, passwordHash)
        return redirect(url_for("userRouter.login"))
    return render_template("singup.html")


@userRouter.route("/login", methods=["GET", "POST"])
@handleError("login faild")
def login():
    if request.method == "POST":
        bcrypt = current_app.extensions["bcrypt"]
        email = request.form.get("email")
        password = request.form.get("password")

        userData = getUserEmail(email)

        if not userData:
            flash("Invalid email", "error")
            return redirect(url_for("userRouter.login"))

        userId, userName, email, passwordHash = userData

        if not bcrypt.check_password_hash(passwordHash, password):
            flash("Invalid eamil or password", "error")
            return redirect(url_for("userRouter.login"))

        token = createToken(userId, email, userName)

        resp = make_response(redirect(url_for("userRouter.dashboard")))
        resp.set_cookie("auth_token",
                        token,
                        httponly=False,
                        secure=False,
                        samesite="Lax")
        return resp
    return render_template("login.html")


@userRouter.route("/dashboard")
@handleError("dashboard error")
@login_required
def dashboard(user):
    return render_template("dashboard.html", user=user)
