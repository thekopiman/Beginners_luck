
from flask import redirect, session, g, request, redirect, url_for
from functools import wraps


def login_required(f):
    
    # Decorate routes to require login.
 
    # https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user") is None:
            return redirect("/home")
        return f(*args, **kwargs)
    return decorated_function
