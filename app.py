from flask import Flask, request, redirect, render_template, url_for
#from helpers import token_required
from cryptography.fernet import Fernet
import os
import requests

app = Flask(__name__)
app.config.from_pyfile('config.py')
CIPHER_SUITE = Fernet(app.config['ENCRYPTION_KEY'], )


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/slack', methods=['POST'])
#@token_required
def slack():
    cipher = CIPHER_SUITE.encrypt(bytes(request.form['command'].split(" ")[1]))

    response = "Success! Your Frame terminal can be found here: {url}".format(
                    url=url_for('frame_terminal', cipher=cipher, _external=True))

    return response


@app.route('/frame/<cipher>', methods=['GET'])
def frame_terminal(cipher):
    url = CIPHER_SUITE.decrypt(bytes(cipher))
    print url
    try:
        req = requests.get(url, headers={"Range": "bytes=0-10"})

        if req.headers["Content-Type"] in ("text/plain", "image/jpeg"):
            frame_app = app.config['FRAME_APPS'][req.headers["Content-Type"]]
        else:
            return redirect(url_for('home'))

    except Exception as e:
        return redirect(url_for('home'))

    return render_template('terminal.html', app=frame_app, url=url)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

