from functools import wraps
from flask import g, request, redirect, url_for

def login_not_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if(g.user is not None and g.user.is_authenticated):
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function 
