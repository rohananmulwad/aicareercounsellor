from functools import wraps
from flask import request, flash, render_template
from utils import decodeToken

def login_required(f):
    @wraps(f)
    def decoratedFunction(*args, **kwargs):
        token = request.cookies.get("auth_token")
        
        if not token:
            flash("please login first")
            return render_template("login.html")
        #in their insted of login put some html page or url
        decoded = decodeToken(token)
        if not decoded:
            flash("session expried , please login again")
            return render_template("login.html")        
        
        return f(*args, user=decoded, **kwargs)
    
    return decoratedFunction
    