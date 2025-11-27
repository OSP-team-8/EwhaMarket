import pyrebase
import json
import time


class DBhandler:
    def __init__(self):
        with open('./authentication/firebase_auth.json') as f:
            config = json.load(f)

        firebase = pyrebase.initialize_app(config)
        self.db = firebase.database()

    # -----------------------------
    # 내부 헬퍼: Firebase key로 쓸 user id 정리
    # -----------------------------
    def _user_key(self, user_id: str) -> str:
        """
        Firebase RTDB 키로 사용할 수 있도록 user_id를 안전하게 변환
        - . $ # [ ] / 는 사용할 수 없음
        - 여기서는 이메일의 '.' 만 간단히 ',' 로 치환
        """
        return user_id.replace('.', ',')

    # -----------------------------
    # 상품
    # -----------------------------
    def insert_item(self, name, data, img_path):
        region = data.get('region', '')  # 시/도
        addr = data.get('addr', '')      # 상세 주소

        item_info = {
            "name": name,
            "price": data.get('price', ''),
            "status": data.get('status', ''),
            "region": region,
            "addr": addr,
            "desc": data.get("desc", ""),
            "seller": data.get("seller", ""),
            "phone": data.get("phone", ""),
            "category": data.get("category", "ETC"),
            "card": data.get("card", "Y"),
            "img_path": img_path or "",
            "created_at": time.time(),
        }

        self.db.child("item").child(name).set(item_info)  # 키 값: name
        print("insert_item:", item_info)
        return True

    def get_items(self):
        items = self.db.child("item").get().val()
        return items or {}

    def get_item_byname(self, name):
        item = self.db.child("item").child(name).get().val()
        return item

    # -----------------------------
    # 찜(wishlist)
    # -----------------------------
    def add_wish(self, user_id, item_id):
        key = self._user_key(user_id)
        self.db.child("wishlist").child(key).child(item_id).set(True)

    def remove_wish(self, user_id, item_id):
        key = self._user_key(user_id)
        self.db.child("wishlist").child(key).child(item_id).remove()

    def get_wishlist_ids(self, user_id):
        key = self._user_key(user_id)
        data = self.db.child("wishlist").child(key).get().val()
        if not data:
            return set()
        return set(data.keys())

    def get_wishlist_items(self, user_id):
        ids = self.get_wishlist_ids(user_id)
        result = []
        for item_id in ids:
            item = self.get_item_byname(item_id)
            if item:
                result.append((item_id, item))
        return result

    # -----------------------------
    # 유저
    # -----------------------------
    def insert_user(self, data, pw):  # 회원가입
        user_info = {
            "id": data['id'],
            "pw": pw,
            "first_name": data['first_name'],
            "last_name": data['last_name']
        }

        if self.user_duplicate_check(str(data['id'])):
            self.db.child("user").push(user_info)
            print(data)
            return True
        else:
            return False

    def user_duplicate_check(self, id_string):
        users = self.db.child("user").get()
        print("users###", users.val())
        if str(users.val()) == "None":
            return True
        else:
            for res in users.each():
                value = res.val()

            if value['id'] == id_string:
                return False
            return True

    def find_user(self, id_, pw_):
        users = self.db.child("user").get()
        for res in users.each():
            value = res.val()
            if value['id'] == id_ and value['pw'] == pw_:
                return True
        return False

    def get_user(self, id_):
        users = self.db.child("user").get()

        for res in users.each():
            value = res.val()
            if value['id'] == id_:
                return value
        return None

    # -----------------------------
    # 리뷰
    # -----------------------------
    def reg_review(self, data, img_path, writer):
        review_info = {
            "item": data['review_item'],          # 상품명
            "title": data['review_title'],        # 리뷰 제목
            "rate": data.get('rating', ''),       # 별점 (문자열일 수도 있음)
            "review": data['review_content'],     # 내용
            "img_path": img_path,                 # 이미지 파일명
            "created_at": time.time(),            # 리뷰 작성 시간
            "writer": writer,                     # 작성자 이름 (닉네임)
        }
        # 제목을 key로 저장 
        self.db.child("review").child(data['review_title']).set(review_info)
        return True

    def get_reviews(self):
        reviews = self.db.child("review").get().val()
        return reviews

    def get_review(self, review_id):
        data = self.db.child("review").child(review_id).get().val()

        if isinstance(data, dict) and ("title" in data or "item" in data):
            return data

        if isinstance(data, dict):
            for _, v in data.items():
                if isinstance(v, dict):
                    return v
        return None
