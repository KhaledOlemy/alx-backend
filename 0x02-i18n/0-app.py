#!/usr/bin/env python3
"""Simple WSGI"""
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def homepage():
    """basic homepage function that renders basic html"""
    return render_template("0-index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
