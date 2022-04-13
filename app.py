from crypt import methods
from pickletools import read_uint1
from flask import Flask, jsonify, render_template, request

from models import user
from models.news import News

app = Flask(__name__)

user_model = user.User()
news_model = News()

@app.route("/")
def index():
  return render_template("index.html")

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

@app.route("/news")
def news():
  news = news_model.find({}, start=0)
  return jsonify(news)

app.run(debug=True)