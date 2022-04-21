from flask import Blueprint, render_template, request
from models.tag_model import Tag


tagBp = Blueprint("tagBp", __name__)

tag_model = Tag()


@tagBp.route("/create_tag", methods=["GET", "POST"])
def create_tag():
    if (request.method == "GET"):
        return render_template("create-tag.html")
    if (request.method == "POST"):
        tagName = request.form.get("name")
        tag_model.create({"name": tagName, "used": 0})
        return render_template("create-tag.html", success=True)
