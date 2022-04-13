

from flask import Flask, jsonify, redirect, render_template, request

from models import user
from models.news import News

app = Flask(__name__)

user_model = user.User()
news_model = News()


def getTrimmedWords(word):
    texts = word.split()

    text = ""
    lastRange = min(len(texts), 20)
    for i in range(0, lastRange):
        text += texts[i] + " "

    return text


@app.route("/")
def index():
    return redirect("/news")


@app.route("/news")
def news():
    startArgs = request.args.get("start")

    start = 0 if startArgs == None else int(startArgs)
    limit = 5
    news = news_model.find({}, start=start * limit, limit=limit)

    for n in news["data"]:
        currentText = n["text"]
        n["text"] = getTrimmedWords(currentText)

    hasMore = news["pagination"]["hasMore"]

    return render_template("index.html", news=news["data"], start=start, hasMore=hasMore)

# Untuk login


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        users = user_model.find({"username": username, "password": password})
        if (len(users) < 1):
            return "User tidak ditemukan"

        user = users[0]
        return "Selamat datang " + user["username"]

# Untuk daftar user


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")

    if request.method == "POST":
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        username = request.form.get("username")
        password = request.form.get("password")

        user_model.create({
            "firstname": firstname,
            "lastname": lastname,
            "username": username,
            "password": password,
        })

        return "User berhasil dibuat"

# Untuk input berita


@app.route("/news/create", methods=["GET", "POST"])
def create_news():
    if request.method == "GET":
        return render_template("create-news.html")

    if request.method == "POST":
        title = request.form.get("title")
        writer = request.form.get("writer")
        text = request.form.get("text")
        category = request.form.get("category")

        newNewsData = {
            "title": title,
            "writer": writer,
            "text": text,
            "category": category,
            "readed": 0
        }
        news_model.create(newNewsData)

        return "Success ditambahkan"


app.run(debug=True)
