import pyrebase
import json 
import time


class DBhandler:
  def __init__(self):
   with open('./authentication/firebase_auth.json') as f:
     config=json.load(f)

   firebase = pyrebase.initialize_app(config)
   self.db = firebase.database()

  def insert_item(self, name, data, img_path): #POST방식으로 넘겨받은 상품정보 firebase db 함수에 추가
   item_info ={
    "seller": data['seller'],
    "addr": data['addr'],
    "email": data['email'],
    "category": data['category'],
    "card": data['card'],
    "status": data['status'],
    "phone": data['phone'],
    "img_path": img_path
 }
   self.db.child("item").child(name).set(item_info)
   print(data,img_path)
   return True
  
  def insert_user(self, data, pw):  # 회원가입
    # data: request.form 그대로 넘어온다고 가정
    user_info = {
        "id": data['id'],                # 로그인에 사용할 아이디(지금은 이메일 칸)
        "pw": pw,                        # 해시된 비밀번호
        "first_name": data['first_name'],# 이름
        "last_name": data['last_name']   # 성
    }

    # 아이디 중복 체크
    if self.user_duplicate_check(str(data['id'])):
        self.db.child("user").push(user_info)
        print(data)
        return True
    else:
        return False
    
  def user_duplicate_check(self, id_string): #user노드에 사용자 정보 등록
    users = self.db.child("user").get()
    print("users###",users.val()) # 첫 등록 시 중복체크 로직 안타게 변경
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
    target_value=[]
    for res in users.each():
        value = res.val()
        if value['id'] == id_ and value['pw'] == pw_:
            return True
    return False

  def get_items(self):
    items = self.db.child("item").get().val()
    return items
  
  def get_item_byname(self, name):
      items = self.db.child("item").get()
      target_value = ""
      print("##########", name)

      for res in items.each():
          key_value = res.key()

          if key_value == name:
              target_value = res.val()

      return target_value
  
  def reg_review(self, data, img_path):
    review_info = {
        "item": data['review_item'],          # 상품명
        "title": data['review_title'],        # 리뷰 제목
        "rate": data.get('rating', ''),       # 별점 (문자열일 수도 있음)
        "review": data['review_content'],     # 내용
        "img_path": img_path,                 # 이미지 파일명
        "created_at": time.time(),            # 리뷰 작성 시간(유닉스 타임스탬프)
    }
    # 제목을 key로 저장 
    self.db.child("review").child(data['review_title']).set(review_info)
    return True


  def get_reviews(self):
    reviews = self.db.child("review").get().val()
    return reviews
  
  def get_review(self, review_id):
    data = self.db.child("review").child(review_id).get().val()

    # 1) 새 구조: 바로 {item, title, rate, review, img_path} 형태면 그대로 반환
    if isinstance(data, dict) and ("title" in data or "item" in data):
        return data

    # 2) 옛날 구조: {"랜덤키": {item, title, rate, review, img_path}} 인 경우
    if isinstance(data, dict):
        for _, v in data.items():
            if isinstance(v, dict):
                return v

    # 3) 아무 것도 못 찾았으면 None
    return None
  
  def get_user(self, id_):
    users = self.db.child("user").get()

    for res in users.each():
        value = res.val()
        if value['id'] == id_:
            return value   # {"id":..., "pw":..., "first_name":..., "last_name":...}

    return None



  
  

