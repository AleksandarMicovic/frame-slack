Frame-Slack Integration
=========================

Flack (Frame + Slack) is a Slack slash command that allows you to edit text files, and images from the net in a single Frame instance.

Installation
------------

Clone the repository:

```
$ git clone docutils
```

Activate virtual env:

```
$ source venv/bin/activate
```

Install all requirements:

```
$ pip install -r requirements.txt
```

Generate a Slack token from their web panel, and export it:

```
$ export SLACK_TOKEN=YOUR_SLACK_TOKEN_HERE
```

Generate an encryption key. Start up a Python interpreter and:

```
from cryptography.fernet import Fernet
key = Fernet.generate_key()
```

Copy the result from above, and then export just like the Slack command:

```
export ENCRYPTION_KEY=YOUR_KEY_HERE
```


Running
-------

To run, simply deploy to heroku:

```
$ git push heroku master
```

or, locally, by:

```
$ python app.py
```


Usage
-----

In slack, simply use `/frame` with a URL like so:

```
/frame http://i.imgur.com/kmwJmi7.jpg
```
