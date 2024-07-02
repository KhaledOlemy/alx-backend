#!/usr/bin/env python3
"""Simple WSGI, a basic flask app"""
from flask import Flask, render_template
from flask_babel import Babel


class Config:
    """Config class/object to config our flask app from"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)


@app.route("/")
def homepage():
    """basic homepage function that renders basic html"""
    return render_template("1-index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
