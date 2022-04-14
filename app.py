

from datetime import timedelta
from threading import Timer
from config import config
from constants import jwt_access_cookie_name
from flask_jwt_extended import create_access_token, JWTManager, get_jwt_identity
import bcrypt
from flask import Flask, redirect, render_template, request, make_response

from models import user
from models.category import Category
from models.news import News

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = config["jwt_secret"]
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=5)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
JWTManager(app)

category_model = Category()
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


def getCategoryFilter(category):
    if (category == None):
        return {}
    else:
        return {"category": category}


@app.route("/news")
def news():
    startArgs = request.args.get("start")
    categoryArgs = request.args.get("category")

    categories = category_model.find({})

    start = 0 if startArgs == None else int(startArgs)
    limit = config["news_limit"]
    news = news_model.find(getCategoryFilter(
        categoryArgs), start=start * limit, limit=limit)
    mostReadedNews = news_model.find(
        {}, start=0, limit=limit, sort=["readed", -1])
    for n in news["data"]:
        currentText = n["text"]
        n["text"] = getTrimmedWords(currentText)
    hasMore = news["pagination"]["hasMore"]
    return render_template("index.html", news=news["data"], start=start, hasMore=hasMore, categories=categories, activeCategory=categoryArgs, mostReadedNews=mostReadedNews["data"])


@app.route("/news/<string:id>")
def news_detail(id):

    news = news_model.find_by_id(id)
    currentReaded = news["readed"]
    news["readed"] = currentReaded + 1
    news.pop("_id")
    news_model.update(id, news)
    return render_template("news_detail.html", news=news)


# Untuk login


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        users = user_model.find({"username": username})
        if (len(users) < 1):
            return render_template("login.html", success=False, message="User tidak ditemukan")

        user = users[0]
        userPass = user["password"]
        userFirstName = user["firstname"]
        userLastName = user["lastname"]
        isPassed = bcrypt.checkpw(password.encode("utf-8"), userPass)
        if (isPassed):
            access_token = create_access_token(identity=userFirstName + " " +
                                               userLastName)
            response = make_response(render_template(
                "login.html", success=True, message="Selamat Datang Fatwa"))
            response.set_cookie(jwt_access_cookie_name, access_token)
            return response

        return render_template("login.html", success=False, message="User tidak ditemukan")

@app.route("/logout")
def logout():
    resp = make_response(render_template("logout.html"))
    resp.delete_cookie(jwt_access_cookie_name)
    return resp

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
        # Hash password
        salt = bcrypt.gensalt()
        password = bcrypt.hashpw(password.encode("utf-8"), salt)

        user_model.create({
            "firstname": firstname,
            "lastname": lastname,
            "username": username,
            "password": password,
        })

        return render_template("signup.html", success=True)

# Untuk input berita


@app.route("/news_create", methods=["GET", "POST"])
def create_news():
    access_token = request.cookies.get(jwt_access_cookie_name)

    if access_token == None:
        return "Login dulu"
    categories = category_model.find({})
    if request.method == "GET":
        return render_template("create-news.html", categories=categories, emptyFields={})

    if request.method == "POST":
        title = request.form.get("title")
        writer = request.form.get("writer")
        text = request.form.get("text")
        category = request.form.get("category")
        if title == None or writer == None or text == None:
            emptyFields = {
                "title": title == None,
                "writer": writer == None,
                "text": text == None,
                "category": category == None,
            }
            return render_template("create-news.html", categories=categories, success=True, emptyFields=emptyFields)

        newNewsData = {
            "title": title,
            "writer": writer,
            "text": text,
            "category": category,
            "readed": 0
        }
        news_model.create(newNewsData)

        return render_template("create-news.html", categories=categories, success=True, emptyFields={})


@app.route("/create_category", methods=["GET", "POST"])
def create_category():
    if request.method == "GET":
        return render_template("create-category.html")

    if request.method == "POST":
        categoryName = request.form.get("name")
        category_model.create({"name": categoryName})
        return render_template("create-category.html", success=True)

app.run(debug=True)
