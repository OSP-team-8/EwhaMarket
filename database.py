import pyrebase
import json 

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