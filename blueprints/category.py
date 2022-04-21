from flask import Blueprint, render_template, request

from models.category import Category

category_model = Category()

categoryBp = Blueprint("categoryBp", __name__)


@categoryBp.route("/create_category", methods=["GET", "POST"])
def create_category():
    if request.method == "GET":
        return render_template("create-category.html")

    if request.method == "POST":
        categoryName = request.form.get("name")
        category_model.create({"name": categoryName})
        return render_template("create-category.html", success=True)
