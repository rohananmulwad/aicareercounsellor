from functools import wraps
from flask import request, flash, redirect, url_for
from utils import decodeToken


def loginRequired(f):
    @wraps(f)
    def decoratedFunction(*args, **kwargs):
        token = request.cookies.get("auth_token")

        if not token:
            flash("please login first")
            # in their insted of login put some html page or url
            return redirect(url_for("userRouter.login"))
        decoded = decodeToken(token)
        if not decoded:
            flash("session expried , please login again")
            return redirect(url_for("userRouter.login"))

        return f(*args, user=decoded, **kwargs)

    return decoratedFunction
