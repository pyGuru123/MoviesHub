import os
import asyncio
from flask import (
    render_template,
    request,
    json,
    jsonify,
    Response,
    flash,
    redirect,
    url_for,
    session,
)

from app import app, db
from app.model import Movie
from app.script import get_movie_url, send_post
from app.utils import download_posts

USERID = os.getenv("USERID")
PASSWORD = os.getenv("PASSWORD")

@app.route("/")
@app.route("/index")
def index():
    if not session.get("userid"):
        return redirect("/login")

    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("userid"):
        return redirect("/index")

    if request.method == "POST":
        userid = request.form.get("username")
        password = request.form.get("password")

        if userid == USERID and password == PASSWORD:
            session["userid"] = userid
            session["password"] = password

            flash(f"Hello Admin, You are now loggedin", "success")
            return redirect("/index")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("userid")
    session.pop("username", None)
    # flash("You logged out succesfully", "success")
    return redirect("/login")


@app.route("/movieurl", methods=["GET", "POST"])
def movieurl():
    if request.method == "POST":
        data = request.get_json()
        name = data["name"]
        url = data["hash"]

        name = name.replace(" ", "+")
        return jsonify({"url": get_movie_url(name, url)})

@app.route("/update", methods=["GET", "POST"])
def update_posts():
    download_posts()
    return redirect("/index")


@app.route("/postbot", methods=["GET", "POST"])
def postbot():
    if request.method == "POST":
        image_url = request.form.get("imageurl")
        caption = request.form.get("caption")
        text480 = request.form.get("text480")
        url480 = request.form.get("url480")
        text720 = request.form.get("text720")
        url720 = request.form.get("url720")
        text1080 = request.form.get("text1080")
        url1080 = request.form.get("url1080")

        buttons = []
        if url480:
            if not url480.startswith("https://moviehubm"):
                url480 = get_movie_url(caption.split()[0], url480)
            buttons.append([text480, url480])

        if url720:
            if not url720.startswith("https://moviehubm"):
                url720 = get_movie_url(caption.split()[0], url720)
            buttons.append([text720, url720])

        if url1080:
            if not url1080.startswith("https://moviehubm"):
                url1080 = get_movie_url(caption.split()[0], url1080)
            buttons.append([text1080, url1080])

        data = {"image_url": image_url, "caption": caption, "buttons": buttons}

        asyncio.run(send_post(data))

    return redirect("/index")

@app.route("/newmovie")
def newmovie():
    movie = Movie(
        img_url="https://www.bollywoodhungama.com/wp-content/uploads/2023/01/Pathaan-2-10.jpg",
        caption="pathann webrip",
        text480p="480p 300mb",
        url480p="hello123",
        text720p="",
        url720p="",
        text1080p="",
        url1080p="")

    movie.save()

# @app.route("/allmovies", methods=["GET", "POST"])
# def allmovies():
#     cursor = collection.find()
#     for data in cursor:
#         print(data)
#     # for 
#     return str(data)

# @app.route("/allposts", methods=["GET", "POST"])
# def allposts():
#     return get_all_posts()