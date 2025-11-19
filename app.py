from flask import Flask, render_template, request, abort, redirect, url_for, flash
from database import DBhandler
import sys

application = Flask(__name__)
application.secret_key = "ewhamarket8"

DB = DBhandler()

# # DB 대신 임시 상품 데이터
# MOCK_PRODUCTS = [
#     {"id": "p1001", "name": "뽀로로 인형 세트", "thumb": "images/뽀로로인형세트.PNG"},
#     {"id": "p1002", "name": "수달 인형", "thumb": "images/수달인형.PNG"},
#     {"id": "p1003", "name": "책 세트", "thumb": "images/책세트.PNG"},
#     {"id": "p1004", "name": "테스트 주도 개발 시작하기",       "thumb": "images/테스트주도개발시작하기.PNG"},
#     {"id": "p1005", "name": "서랍장", "thumb": "images/서랍장.PNG"},
#     {"id": "p1006", "name": "팔찌", "thumb": "images/팔찌.PNG"},
# ]


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

    #결과 화면 로그 생성
    print("====== 상품 등록 데이터 수신 ======")
    print(f"Item name: {data.get('name')}")
    print(f"Seller ID: {data.get('seller')}")
    print(f"Address: {data.get('addr')}")
    print(f"Email: {data.get('email')}")
    print(f"Category: {data.get('category')}")
    print(f"Credit Card?: {data.get('card')}")
    print(f"Status: {data.get('status')}")
    print(f"Phone: {data.get('phone')}")
    print(f"Image Filename: {image_file.filename}")
    print("===================================")
    
    return render_template("submit_item_result.html", data = data,
                        img_path = "static/images/{}".format(image_file.filename))

if __name__ == "__main__":
    application.run(host="0.0.0.0")