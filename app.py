from flask import Flask, render_template, request, abort, flash, redirect, url_for, session
from database import DBhandler
import hashlib
import sys

application = Flask(__name__)
application.config["SECRET_KEY"] = "helloosp"
DB = DBhandler()

@application.route("/")
def hello():
    return render_template("login.html") #index.html을 홈화면에 연결


def find_product(pid): #
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


@application.route("/list")
def view_list():
    # MOCK 함수 오류나서 일단 뺌. 이후 수정 필요
    return render_template("list.html")

@application.route("/detail/<pid>")
def product_detail(pid):
    product = find_product(pid)
    if not product:
        abort(404)
    return render_template("product_detail.html", product=product)

@application.route("/product_detail")
def view_product_detail():
    return render_template("product_detail.html")

@application.route("/review")
def view_review():
    # 페이지 번호 (사용자에게는 1페이지부터 보이도록)
    page = request.args.get("page", 1, type=int)

    per_page = 6      # 한 페이지에 보여줄 리뷰 수

    data = DB.get_reviews() or {}   # dict: {제목: 리뷰정보}
    items = list(data.items())      # [(key, info), ...]
    total = len(items)

    # 페이지 슬라이스
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    page_items = items[start_idx:end_idx]

    # 템플릿에서 쓰기 쉽게 리스트로 변환
    reviews = []
    for key, info in page_items:
        obj = info.copy()
        obj['id'] = key   # 필요하면 상세조회에 쓸 수 있음
        reviews.append(obj)

    # 총 페이지 수
    page_count = (total + per_page - 1) // per_page if total > 0 else 1

    return render_template(
        "review.html",
        reviews=reviews,
        page=page,
        page_count=page_count,
        total=total
    )

@application.route("/review_detail/<review_id>")
def review_detail(review_id):
    review = DB.get_review(review_id)
    if not review:
        abort(404)
    return render_template("review_detail.html", review=review)

@application.route("/reg_items")
def reg_item():
    return render_template("reg_items.html")

@application.route("/reg_reviews")
def reg_reviews_legacy():
    # 예전 주소(/reg_reviews)로 들어와도 새 라우트로 보내기
    return redirect(url_for('reg_review_init'))


# 리뷰 작성 화면 진입 (상품 상세에서 넘어올 때만 name 파라미터 채워짐)
@application.route("/reg_review_init/", defaults={'name': None})
@application.route("/reg_review_init/<name>/")
def reg_review_init(name):
    # name: 상품 이름 (상품 상세에서 넘어올 때만 채워짐)
    return render_template("reg_reviews.html", name=name)

# 리뷰 등록 처리
@application.route("/reg_review", methods=['POST'])
def reg_review():
    data = request.form              # review_item, review_title, rating, review_content
    image_file = request.files.get("file")

    img_filename = ""
    if image_file and image_file.filename != "":
        img_filename = image_file.filename
        image_file.save(f"static/images/{img_filename}")

    # DB에 리뷰 저장
    DB.reg_review(data, img_filename)

    # 저장 후 전체 리뷰 화면으로 이동 
    return redirect(url_for('view_review'))

@application.route("/login")
def view_login():
    return render_template("login.html")

@application.route("/login_confirm", methods=['POST'])
def login_user():
    id_=request.form['id']
    pw=request.form['pw']
    pw_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()
    if DB.find_user(id_,pw_hash):
        session['id']=id_
        return redirect(url_for('view_list'))
    else:
        flash("Wrong ID or PW!")
        return render_template("login.html")
    
@application.route("/logout")
def logout_user():
    session.clear()
    return redirect(url_for('view_list'))

@application.route("/signup")
def view_signup():
    return render_template("signup.html")

@application.route("/signup_post", methods=['POST'])
def register_user():
    data = request.form

    # 비밀번호
    pw = request.form['pw']
    pw2 = request.form.get('pw2')

    # 비밀번호 확인 체크 (폼에 pw2 인풋 있다고 가정)
    if pw2 is not None and pw != pw2:
        flash("비밀번호 확인이 일치하지 않습니다.")
        return render_template("signup.html")

    # 비밀번호 해시
    pw_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()

    # DB에 사용자 정보 저장 시도
    if DB.insert_user(data, pw_hash):
        # 가입 성공하면 로그인 화면으로
        flash("회원가입이 완료되었습니다. 로그인해 주세요.")
        return render_template("login.html")
    else:
        # 아이디 중복인 경우
        flash("이미 존재하는 아이디입니다.")
        return render_template("signup.html")

@application.route("/wishlist")
def view_wishlist():
    return render_template("wishlist.html")

@application.route("/submit_item", methods=['POST'])
def reg_item_submit():

    image_file = request.files["file"]
    image_file.save("static/images/{}".format(image_file.filename))
    data = request.form

    DB.insert_item(data['name'], data, image_file.filename)

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