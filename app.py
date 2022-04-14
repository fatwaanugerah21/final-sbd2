

from config import config
from constants import jwt_access_cookie_name
from flask_jwt_extended import create_access_token, JWTManager, current_user, decode_token, verify_jwt_in_request
import bcrypt
from flask import Flask, redirect, render_template, request, make_response

from models import user
from models.category import Category
from models.news import News

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = config["jwt_secret"]
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
    return render_template("index.html", news=news["data"], start=start, hasMore=hasMore, categories=categories, activeCategory=categoryArgs, mostReadedNews=mostReadedNews)


@app.route("/news/<string:id>")
def news_detail(id):
    news = news_model.find_by_id(id)
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

        return "User berhasil dibuat"

# Untuk input berita


@app.route("/news/create", methods=["GET", "POST"])
def create_news():
    access_token = request.cookies.get(jwt_access_cookie_name)
    decoded = decode_token(access_token)

    if access_token == None:
        return "Login dulu"
    if request.method == "GET":
        categories = category_model.find({})
        return render_template("create-news.html", categories=categories)

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


@app.route("/category/create", methods=["GET", "POST"])
def create_category():
    if request.method == "GET":
        return render_template("create-category.html")

    if request.method == "POST":
        categoryName = request.form.get("name")
        category_model.create({"name": categoryName})
        return "Kategori success ditambahkan"


app.run(debug=True)
