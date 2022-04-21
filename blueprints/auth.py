import bcrypt
from flask import Blueprint, make_response, render_template, request
from flask_jwt_extended import create_access_token
from constants import jwt_access_cookie_name
from models.user import User


user_model = User()

authBp = Blueprint("authBp", __name__)


@authBp.route("/logout")
def logout():
    resp = make_response(render_template("logout.html"))
    resp.delete_cookie(jwt_access_cookie_name)
    return resp

# Untuk daftar user


@authBp.route("/signup", methods=["GET", "POST"])
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

# Untuk login


@authBp.route("/login", methods=["GET", "POST"])
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
