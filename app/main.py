import hashlib
import json

from flask import render_template, request, url_for, session
from flask_login import login_user
from sqlalchemy import true

from app import app, login
from app.dao import timkiem, add_user, list_theloai, check_user
from app.models import *


#######################MAPMING####################################


@app.route("/", methods=['GET', 'POST'])
def index():
    theloai = Loaisach.query.all()
    return render_template("ogani/index.html", theloai1=theloai, athome="active")


@app.route('/shop-grid', methods=['GET', 'POST'])
def shop_grid():
    return render_template('ogani/shop-grid.html', theloai1=list_theloai(), atgrid="active")


@app.route('/shop-details', methods=['GET', 'POST'])
def shop_details():
    if request.method == 'POST':
        return redirect(url_for('shop-grid'))
    return render_template('ogani/shop-details.html', theloai1=list_theloai(), atdt="active")


@app.route('/shoping-cart', methods=['GET', 'POST'])
def shoping_cart():
    if request.method == 'POST':
        return redirect(url_for('shop-grid'))
    return render_template('ogani/shoping-cart.html', theloai1=list_theloai(), atgrid="active")


@app.route('/blog', methods=['GET', 'POST'])
def blog():
    if request.method == 'POST':
        return redirect(url_for('shop-grid'))
    return render_template('ogani/blog.html', theloai1=list_theloai(), atgrid="active")


@app.route("/login-admin", methods=["POST", "GET"])
def login_admin():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        password = str(hashlib.md5(password.strip().encode("utf-8")).hexdigest())
        # truy van tach sang dao.py
        user = User.query.filter(User.username == username.strip(), User.password == password).first()
        if user:
            login_user(user=user)

    return redirect("/admin")


@app.route("/check-login", methods=["POST", "GET"])
def check_login1():
    username = request.args.get("username")
    password = request.args.get("pass")
    user = User.query.filter(User.username == "admin2").first()
    if user:
        session["user"] = json.dumps(user)
        return redirect(url_for('index'))
    else:
        err_msg = "ĐĂng nhập không thành công"

    return render_template("Login/login.html", err_msg=err_msg)


@app.route("/login", methods=["POST", "GET"])
def login1():
    return render_template("Login/login.html")


@app.route("/signin", methods=["POST", "GET"])
def signin():
    return render_template("Login/signin.html")


@app.route("/signin/add", methods=["POST", "GET"])
def signin_add():
    if request.method.lower() == "get":
        name = request.args.get("name")
        username = request.args.get("username")
        password = request.args.get("pass")
        add_user(name, username, password)
        return redirect("/")

    return render_template("Login/signin.html")


######################WOKING###############################

# Tìm kiếm sách theo loại
@app.route("/sach", methods=['GET', 'POST'])
def sach():
    kw = request.args.get("keyword")
    loai = request.args.get("loai")
    list = Sach.query.filter(Sach.tensach == kw)
    posts = timkiem(loai, kw)
    dem = posts.count()
    return render_template("ogani/shop-grid.html", theloai1=list_theloai(), listsach=posts, tong=dem)


@app.route("/shop-grid1", methods=['GET', 'POST'])
def theloai():
    kw = request.args.get("key")
    posts = timkiem("test", kw)
    dem = posts.count()
    return render_template("ogani/shop-grid.html", theloai1=list_theloai(), listsach=posts, tong=dem)


@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)


if __name__ == "__main__":
    app.run(debug=True)
