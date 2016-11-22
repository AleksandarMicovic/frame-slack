import requests
from functools import wraps
from flask import request, redirect, url_for
from config import SLACK_TOKEN, FRAME_APPS


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


def get_url_mimetype(url):
    mimetype = None

    try:
        req = requests.get(url, headers={"Range": "bytes=0-10"})
        mimetype = req.headers["Content-Type"]

        if ";" in mimetype:
            mimetype = mimetype.split(";")[0]

    except Exception as e:
        mimetype = False

    return mimetype
