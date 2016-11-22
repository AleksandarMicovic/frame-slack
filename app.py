from flask import Flask, request, redirect, render_template, url_for
import requests

app = Flask(__name__)
app.config.from_pyfile('config.py')


@app.route('/')
def home():
    # Will also serve as the page for errors.
    return "HOME FOR EVERYTHING :)"


@app.route('/slack', methods=['POST'])
@token_required
def slack():
    url = request.form['command'].split(" ")[1]
    response = "Your Frame app can be found at: " +\
               url_for(frame_terminal, url=url)

    return response
        

@app.route('/frame', methods=['GET'])
def frame_terminal():
    req = None
    frame_app = None

    try:
        req = requests.get(request.args.get('url'),
                           headers={"Range": "bytes=0-10"})

        print req.headers["Content-Type"]

        if req.headers["Content-Type"] in ("text/plain", "image/jpeg"):
            frame_app = app.config['FRAME_APPS'][req.headers["Content-Type"]]
        else:
            return redirect(url_for('home'))

    except Exception as e:
        return redirect(url_for('home'))

    return render_template('terminal.html', app=frame_app)


if __name__ == '__main__':
    app.run(host='0.0.0.0')

