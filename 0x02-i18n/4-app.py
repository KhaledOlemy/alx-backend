#!/usr/bin/env python3
"""Simple WSGI, a basic flask app"""
from flask import Flask, render_template, request
from flask_babel import Babel


class Config:
    """Config class/object to config our flask app from"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)


@babel.localeselector
def get_locale():
    """Gets the most matching locale based on request headers"""
    q_lng = request.query_string.decode().split('locale=')[-1].split('&')[0]
    if q_lng and q_lng in app.config["LANGUAGES"]:
        return q_lng
    return request.accept_languages.best_match(app.config["LANGUAGES"])


@app.route("/")
def homepage():
    """basic homepage function that renders basic html"""
    return render_template("4-index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
