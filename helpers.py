from functools import wraps
from flask import request, redirect, url_for
from config import SLACK_TOKEN


def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # TODO: TRY EXCEPT HERE
        if request.form['SLACK_TOKEN'] != SLACK_TOKEN:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function
