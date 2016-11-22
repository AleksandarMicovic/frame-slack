from functools import wraps
from flask import request, redirect, url_for
from config import SLACK_TOKEN


def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            if request.form['token'] != SLACK_TOKEN:
                return redirect(url_for('home'))
        except:
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function
