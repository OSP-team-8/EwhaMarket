# database.py
import pyrebase
import json

class DBhandler:
    def __init__(self):
        with open('./authentication/firebase_auth.json') as f:
            config = json.load(f)

        firebase = pyrebase.initialize_app(config)
        self.db = firebase.database()

    # 상품 등록
    def insert_item(self, name, data, img_path):
        full_addr = f"{data.get('region', '')} {data.get('addr', '')}".strip()

        item_info = {
            "name": name,                           
            "price": data.get("price"),             
            "status": data.get("status"),           # 상태 (new / lnew / used)

            "region": data.get("region"),           
            "addr": data.get("addr"),               
            "full_addr": full_addr,                 # 합쳐진 주소 

            "desc": data.get("desc"),               
            "seller": data.get("seller"),           
            "phone": data.get("phone"),                    

            "img_path": img_path                  
        }

        self.db.child("item").child(name).set(item_info)
        print("insert_item:", item_info)
        return True

    # 상품 목록 조회
    def get_item_list(self, q = None):
        res = self.db.child("item").get()

        if not res.each():
            return []
        
        products = []

        for r in res.each():
            key = r.key()
            data = r.val()

            # 검색 조건
            if q:
                q_lower = q.lower()
                name = (data.get("name") or "").lower()
                desc = (data.get("desc") or "").lower()
                if q_lower not in name and q_lower not in desc:
                    continue

            img_name = data.get("img_path")
            thumb = None
            if img_name:
                thumb = f"images/{img_name}"

            products.append({
                "id": key,
                "name": data.get("name", key),
                "thumb" : thumb
            })

        return products
    
    # 상품 상세 조회
    def get_item(self, pid):
        res = self.db.child("item").child(pid).get()
        data = res.val()

        if not data:
            return None
        
        img_name = data.get("img_path")
        thumb = None
        if img_name:
            thumb = f"images/{img_name}"

        return {
            "id": pid,
            "name": data.get("name"),
            "price": data.get("price"),
            "status": data.get("status"),
            "region": data.get("region"),
            "addr": data.get("addr"),
            "full_addr": data.get("full_addr"),
            "desc": data.get("desc"),
            "seller": data.get("seller"),
            "phone": data.get("phone"),
            "thumb": thumb,
        }
