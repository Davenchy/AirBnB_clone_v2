#!/usr/bin/python3
"""Starts flask web server on port 5000"""

from flask import Flask

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/')
def home():
    """Home route, returns Hello HBNB"""
    return "Hello HBNB!"


@app.route('/hbnb')
def hbnb_route():
    """route returns HBNB"""
    return "HBNB"


@app.route('/c/<text>')
def c_route(text):
    """route returns text"""
    return "C {}".format(text.replace('_', ' '))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)