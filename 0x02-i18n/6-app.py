#!/usr/bin/env python3
"""Simple WSGI, a basic flask app"""
from flask import Flask, render_template, request, g
from flask_babel import Babel


class Config:
    """Config class/object to config our flask app from"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)


users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user():
    login_as = request.args.get("login_as")
    if login_as:
        return users.get(int(login_as))
    return None


@app.before_request
def before_request():
    user = get_user()
    g.user = user


@babel.localeselector
def get_locale():
    """Gets the most matching locale based on request headers"""
    q_lng = request.args.get('locale')
    if q_lng and q_lng in app.config["LANGUAGES"]:
        return q_lng
    if g.user and g.user.get("locale") in app.config["LANGUAGES"]:
        return g.user.get("locale")
    return request.accept_languages.best_match(app.config["LANGUAGES"])


@app.route("/")
def homepage():
    """basic homepage function that renders basic html"""
    return render_template("6-index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
