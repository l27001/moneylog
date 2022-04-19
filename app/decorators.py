from functools import wraps
from flask import g, request, redirect, url_for, flash

def login_not_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if(g.user is not None and g.user.is_authenticated and not g.user.is_anonymous):
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function 

def guest_not_allowed(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if(g.user is not None and g.user.id == 0):
            if(request.method != "POST"):
                flash("Гость не может выполнять это действие", "danger")
                return redirect(url_for("index"))
            else:
                return {"status":"fail", "description":"Гость не может выполнять это действие"}
        return f(*args, **kwargs)
    return decorated_function 
