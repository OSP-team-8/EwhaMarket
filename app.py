from flask import Flask, render_template, request, abort, flash, redirect, url_for, session
from database import DBhandler
import hashlib
import sys
import math

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
    q = request.args.get("q", "", type = str).strip()

    page = request.args.get("page", 1, type=int)
    if page < 1:
        page = 1
    per_page = 6    

    data = DB.get_items()
    items = list(data.items())

    #검색 필터링
    if q:
        q_lower = q.lower()

        def match(info):
            name = str(info.get("name", "")).lower()
            desc = str(info.get("desc", "")).lower()
            region = str(info.get("region", "")).lower()
            seller = str(info.get("seller", "")).lower()
            return (
                q_lower in name
                or q_lower in desc
                or q_lower in region
                or q_lower in seller
            )
        items = [(k,v) for (k,v) in items if match(v)]

    total = len(items)

    #최신순 정렬
    def get_created_at(info):
        try: 
            return float(info.get("created_at", 0))
        except (TypeError, ValueError):
            return 0.0
        
    items.sort(key=lambda kv: get_created_at(kv[1]), reverse = True)

    #paging
    start_idx = (page -1) * per_page
    end_idx = start_idx + per_page
    page_items = items[start_idx:end_idx]

    #로그인한 유저의 찜 목록 아이디
    user_id = session.get('id')
    liked_ids = DB.get_wishlist_ids(user_id) if user_id else set()

    products = []
    for item_id, info in page_items:
        img_filename = info.get("img_path") or ""
        thumb_path = f"images/{img_filename}" if img_filename else None

        products.append({
            "id": item_id,                     # URL 파라미터용
            "name": info.get("name", item_id),
            "thumb": thumb_path,              # url_for('static', filename=p.thumb)
            "price": info.get("price", 0),    # 나중에 목록에서 가격 쓰고 싶으면 사용
            "status": info.get("status", ""),
            "region": info.get("region", ""),
            "liked": (item_id in liked_ids),
        })

    page_count = (total + per_page -1) // per_page if total > 0 else 1

    return render_template(
        "list.html",
        products = products,
        page = page,
        page_count = page_count,
    )

@application.route("/wish/<pid>", methods = ['POST'])
def toggle_wish(pid):
    userId = session.get('id')
    if not userId:
        flash("로그인 후 이용 가능합니다.")
        return redirect(url_for('view_login'))
    
    liked_ids = DB.get_wishlist_ids(userId)

    if pid in liked_ids:
        DB.remove_wish(userId, pid)
        flash("찜이 취소되었습니다.")
    else: 
        DB.add_wish(userId, pid)
        flash("찜 목록에 추가되었습니다.")

    next_url = request.referrer or url_for('view_list')
    return redirect(next_url)

@application.route("/detail/<pid>")
def product_detail(pid):
    item = DB.get_item_byname(pid)
    if not item:
        abort(404)

    try:
        price_int = int(item.get("price", 0))
    except (TypeError, ValueError):
        price_int = 0

    img_filename = item.get("img_path") or ""
    thumb_path = f"images/{img_filename}" if img_filename else None

    region_text = (item.get("region", "") or "").strip()
    addr_text = (item.get("addr", "") or "").strip()

    if region_text and addr_text:
        full_address = f"{region_text} {addr_text}"
    else:
        full_address = region_text or addr_text

    user_id = session.get('id')
    liked = False

    if user_id:
        liked_ids = DB.get_wishlist_ids(user_id)
        liked  = pid in liked_ids
    

    product = {
        "id": pid,
        "name": item.get("name", pid),
        "price": price_int,
        "status": item.get("status", ""),
        "desc": item.get("desc", ""),
        "seller": item.get("seller", ""),
        "phone": item.get("phone", ""),
        "region": full_address,
        "thumb": thumb_path,
    }

    return render_template("product_detail.html", product = product, liked = liked)
    
@application.route("/product_detail")
def view_product_detail():
    return render_template("product_detail.html")

@application.route("/review")
def view_review():
    # 정렬 기준: new(최신순, 기본값) / old(오래된순)
    sort = request.args.get("sort", "new")
    # 검색어
    q = request.args.get("q", "", type=str).strip()

    # 페이지 번호 (1페이지부터)
    page = request.args.get("page", 1, type=int)
    if page < 1:
        page = 1

    per_page = 6  # 한 페이지에 보여줄 리뷰 수

    # 1) 전체 리뷰 가져오기
    data = DB.get_reviews() or {}      # dict: {제목: 리뷰정보}
    items = list(data.items())         # [(key, info), ...]
    total_all = len(items)             # 전체 리뷰 개수

    # 2) 검색 필터링
    if q:
        q_lower = q.lower()

        def match(info):
            title = str(info.get("title", "")).lower()
            content = str(info.get("review", "")).lower()
            item_name = str(info.get("item", "")).lower()
            writer = str(info.get("writer", "")).lower()   
            return (
                q_lower in title
                or q_lower in content
                or q_lower in item_name
                or q_lower in writer
            )

        items = [(k, v) for (k, v) in items if match(v)]

    # 검색 이후 개수
    total = len(items)

    # 3) created_at 기준 정렬
    def get_created_at(info):
        try:
            return float(info.get("created_at", 0))
        except (TypeError, ValueError):
            return 0.0

    # 최신순(new) = 내림차순, 오래된순(old) = 오름차순
    reverse = True   # 기본: 최신순
    if sort == "old":
        reverse = False

    items.sort(key=lambda kv: get_created_at(kv[1]), reverse=reverse)

    # 4) 페이지 슬라이스
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    page_items = items[start_idx:end_idx]

    # 5) 템플릿에서 쓰기 쉽게 리스트로 변환
    reviews = []
    for key, info in page_items:
        obj = info.copy()
        obj["id"] = key   # 상세조회에 사용
        reviews.append(obj)

    # 6) 총 페이지 수 (검색 결과 기준)
    page_count = (total + per_page - 1) // per_page if total > 0 else 1

    return render_template(
        "review.html",
        reviews=reviews,
        page=page,
        page_count=page_count,
        total=total,         # 검색 결과 개수
        total_all=total_all, # 전체 리뷰 개수 (필요하면 상단에 사용)
        sort=sort,           # 🔥 템플릿에서 지금 정렬상태 알 수 있게 넘겨줌
        q=q,                 # 검색창에 기존 검색어 유지용
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

     # 세션에서 작성자 이름 만들기
    first = session.get('first_name', '')
    last = session.get('last_name', '')
    if first or last:
        writer = f"{last}{first}".strip()
    else:
        writer = "익명"

    # DB에 리뷰 저장 (작성자 같이 넘김)
    DB.reg_review(data, img_filename, writer)

    # 저장 후 전체 리뷰 화면으로 이동 
    return redirect(url_for('view_review'))



@application.route("/login")
def view_login():
    return render_template("login.html")

@application.route("/login_confirm", methods=['POST'])
def login_user():
    id_ = request.form['id']
    pw = request.form['pw']
    pw_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()

    if DB.find_user(id_, pw_hash):   # 로그인 성공하면
        user = DB.get_user(id_)
        if user:
            session['id'] = id_
            session['first_name'] = user['first_name']
            session['last_name'] = user['last_name']
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
    user_id = session.get('id')
    if not user_id:
        flash("로그인 후 이용 가능합니다.")
        return redirect(url_for('view_login'))
    
    page = request.args.get("page", 1, type = int)
    if page < 1:
        page = 1
    per_page = 5
    
    wish_items = DB.get_wishlist_items(user_id)
    total = len(wish_items)

    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    page_items = wish_items[start_idx:end_idx]

    items = []
    for item_id, info in wish_items:
        img_filename = info.get("img_path") or ""
        thumb_path = f"images/{img_filename}" if img_filename else None

        try:
            price_int = int(info.get("price", 0))
        except (TypeError, ValueError):
            price_int = 0

        items.append({
                       "id": item_id,
            "name": info.get("name", item_id),
            "thumb": thumb_path,
            "price": price_int,
        })

    page_count = (total + per_page - 1) //per_page if total >0 else 1

    return render_template("wishlist.html", 
                           items = items,
                           page = page,
                           page_count = page,
                           total = total,
                           )

@application.route("/submit_item", methods=['POST'])
def reg_item_submit():
    data = request.form

    #이미지 파일 처리
    image_file = request.files.get("file")
    img_filename = ""
    if image_file and image_file.filename != "":
        img_filename = image_file.filename
        image_file.save(f"static/images/{img_filename}")

    DB.insert_item(data['name'], data, img_filename)
    
    return redirect(url_for("view_list"))
if __name__ == "__main__":
    application.run(host="0.0.0.0")