from flask import Flask, render_template, request, abort, redirect, url_for, flash
from database import DBhandler
import sys

application = Flask(__name__)
application.secret_key = "ewhamarket8"

DB = DBhandler()


def find_product(pid):
    for p in MOCK_PRODUCTS:
        if p["id"] == pid:
            p = p.copy()
            p.setdefault("price", 0)
            p.setdefault("status", "")
            p.setdefault("desc", "")
            p.setdefault("seller", "")
            p.setdefault("phone", "")
            p.setdefault("region", "")
            return p
    return None

@application.route("/")
def hello():
    return render_template("login.html") #index.html을 홈화면에 연결

@application.route("/items", methods = ["GET"])
def view_list():
    q = request.args.get("q", "").strip()
    products = DB.get_item_list(q if q else None)

    return render_template("list.html", products = products)

@application.route("/items/<pid>", methods = ["GET"])
def product_detail(pid):
    product = DB.get_item(pid)
    if product is None:
        abort(404)
    return render_template("product_detail.html", product=product)

@application.route("/product_detail")
def view_product_detail():
    return render_template("product_detail.html")

@application.route("/review")
def view_review():
    return render_template("review.html")

@application.route("/review_detail")
def view_review_detail():
    return render_template("review_detail.html")

@application.route("/reg_items")
def reg_item():
    return render_template("reg_items.html")

@application.route("/reg_reviews")
def reg_review():
    return render_template("reg_reviews.html")

@application.route("/login")
def view_login():
    return render_template("login.html")

@application.route("/signup")
def view_signup():
    return render_template("signup.html")

@application.route("/wishlist")
def view_wishlist():
    return render_template("wishlist.html")

@application.route("/submit_item", methods=['POST'])
def reg_item_submit():

    image_file = request.files.get("file")
    img_filename = None
    img_path = None

    if image_file and image_file.filename != "":
        filename = image_file.filename
        img_path = f"static/images/{filename}"
        image_file.save(img_path)
        img_filename = filename
    
    form_data = request.form

    DB.insert_item(form_data["name"], form_data, img_filename)

    return redirect(url_for("view_list"))

if __name__ == "__main__":
    application.run(host="0.0.0.0")