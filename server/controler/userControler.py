from flask import Blueprint,request,render_template,redirect,url_for
from utils import decodeToken,createToken, handleError
from db import getUser, getUserEmail,insertUser,createTable
from app import bcrypt

userRouter = Blueprint("userRouter", __name__, url_prefix="/users")


@userRouter.route("/signup", methods=["GET", "POST"])
@handleError("Signup faild")
def signup():
    if request.method == "POST":
        userName = request.form.get("userName")
        email = request.form.get("email")
        password = request.form.get("password")
        passwordHash = bcrypt.generate_password_hash(password).decode('utf-8')
        insertUser(userName, email, passwordHash)
        return redirect(url_for("userRouter.login"))
    return render_template("singup.html")

