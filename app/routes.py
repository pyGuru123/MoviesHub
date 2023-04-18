from flask import render_template, request, json, jsonify, Response, flash, redirect, url_for, session

from app import app
from app.script import get_movie_url


@app.route("/")
@app.route("/index")
@app.route("/home")
def index():
    return render_template("index.html", shorten_url=None)

@app.route("/movieurl", methods=["GET", "POST"])
def movieurl():
    if request.method == "POST":
        name = request.form["moviename"]
        url = request.form["moviehash"]
        shorten_url = get_movie_url(name, url)

        return render_template("index.html", shorten_url=shorten_url)