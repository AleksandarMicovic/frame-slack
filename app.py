import os
import requests
from flask import Flask, request, redirect, render_template, url_for, jsonify
from helpers import token_required, get_url_mimetype
from cryptography.fernet import Fernet

app = Flask(__name__)
app.config.from_pyfile('config.py')
CIPHER_SUITE = Fernet(app.config['ENCRYPTION_KEY'])


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/slack', methods=['POST'])
@token_required
def slack():
    try:
        user_url = request.form['text']

        if ' ' in user_url:
            user_url = url.split(' ')[0]

        if get_url_mimetype(user_url) in app.config['FRAME_APPS'].keys():
            cipher = CIPHER_SUITE.encrypt(bytes(user_url))
            response = "Success! Your Frame terminal can be found here: {url}".format(
                url=url_for('frame_terminal', cipher=cipher, _external=True))
        else:
            response = "There is a problem with your URL. Try submitting a URL " + \
                       "with nothing else, and ensure that it's an image or a text file."
    except KeyError as e:
        # No text parameter means we aren't being called by Slack.
        return redirect(url_for('home'))

    to_user = {
        "text": response
    }

    return jsonify(to_user)


@app.route('/frame/<cipher>', methods=['GET'])
def frame_terminal(cipher):
    try:
        url = CIPHER_SUITE.decrypt(bytes(cipher))
        frame_app = app.config['FRAME_APPS'][get_url_mimetype(url)]
    except:
        return redirect(url_for('home'))

    return render_template('terminal.html', app=frame_app, url=url)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

