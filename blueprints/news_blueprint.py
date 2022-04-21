from flask import Blueprint, render_template, request
from constants import jwt_access_cookie_name
from config import config
from functions import getCategoryFilter, getTagFilter, getTrimmedWords

from models.category_model import Category
from models.news_model import News
from models.tag_model import Tag

category_model = Category()
tag_model = Tag()
news_model = News()

newsBp = Blueprint("newsBp", __name__)


@newsBp.route("/news")
def news():
    startArgs = request.args.get("start")
    categoryArgs = request.args.get("category")
    tagArgs = request.args.get("tag")

    categories = category_model.find({})
    tags = tag_model.get_10_favourites({})

    start = 0 if startArgs == None else int(startArgs)
    limit = config["news_limit"]

    filter = {}
    filter = getCategoryFilter(filter,
                               categoryArgs)
    filter = getTagFilter(filter,
                          tagArgs)
    news = news_model.find(filter, start=start * limit, limit=limit)
    print(news)
    mostReadedNews = news_model.find(
        {}, start=0, limit=limit, sort=["readed", -1])
    for n in news["data"]:
        currentText = n["text"]
        n["text"] = getTrimmedWords(currentText)
    hasMore = news["pagination"]["hasMore"]
    return render_template("index.html", news=news["data"], start=start, hasMore=hasMore, categories=categories, activeCategory=categoryArgs, mostReadedNews=mostReadedNews["data"], tags=tags)


@newsBp.route("/news/<string:id>")
def news_detail(id):

    news = news_model.find_by_id(id)
    currentReaded = news["readed"]
    news["readed"] = currentReaded + 1
    news.pop("_id")
    news_model.update(id, news)
    return render_template("news_detail.html", news=news)


# Untuk input berita


@newsBp.route("/news_create", methods=["GET", "POST"])
def create_news():
    access_token = request.cookies.get(jwt_access_cookie_name)

    if access_token == None:
        return "Login dulu"

    tags = tag_model.find({})
    categories = category_model.find({})

    if request.method == "GET":
        return render_template("create-news.html", categories=categories, tags=tags, emptyFields={})

    if request.method == "POST":
        title = request.form.get("title")
        writer = request.form.get("writer")
        text = request.form.get("text")
        category = request.form.get("category")
        tags = request.form.getlist("tags")

        if not title or not writer or not text or not tags:
            emptyFields = {
                "title": not title ,
                "writer": not writer ,
                "text": not text ,
                "category": not category ,
                "tags": not tags ,
            }
            return render_template("create-news.html", categories=categories, success=False, emptyFields=emptyFields)

        for t in tags:
            dbTags = tag_model.find({"name": t})
            tag = dbTags[0]
            tagId = tag["_id"]
            tag["used"] += 1
            tag.pop("_id")
            tag_model.update(tagId, tag)

        newNewsData = {
            "title": title,
            "writer": writer,
            "text": text,
            "category": category,
            "tags": tags,
            "readed": 0
        }
        news_model.create(newNewsData)

        return render_template("create-news.html", categories=categories, success=True, emptyFields={})
