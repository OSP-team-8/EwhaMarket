# 📦 Ewha Market

**Ewha Market**은 사용자가 중고 상품을 등록하고, 조회하고거나 리뷰를 등록 조회할 수 있고 관심있는 상품에 대해서는 북마크 기능을 활용할 수 있는 **웹 기반 중고 거래 서비스**입니다.
경량 백엔드 프레임워크 **Flask**와 **Google Firebase** 를 기반으로 서버 비용 없이 안정적이고 빠른 서비스를 구현하였습니다.
프론트엔드는 **HTML/CSS**을 사용하여 구축했습니다.

---

## 🚀 주요 기능

### 👤 사용자 인증

* 이메일 기반 회원가입 (비밀번호 해시 처리)
* 로그인 / 로그아웃
<img width="1710" height="1107" alt="스크린샷 2025-12-07 오전 1 01 56" src="https://github.com/user-attachments/assets/4663bd62-68db-468b-a001-3aad2041e22a" />


### 📦 상품 기능

* 상품 등록 (이미지 업로드 포함)
* 상품 목록 조회 (최신순 / 오래된순)
* 검색 가능
* 페이지네이션
* 상품 상세 조회
<img width="1710" height="1107" alt="스크린샷 2025-12-07 오전 1 02 10" src="https://github.com/user-attachments/assets/a4178799-9e23-4c8a-8ddc-7313c712efd9" />


### ⭐ 리뷰 기능

* 리뷰 작성 (이미지 업로드 포함)
* 리뷰 목록 조회 (오래된순 / 최신순)
* 리뷰 상세 조회
* 페이지네이션
* 검색 가능
<img width="1710" height="1107" alt="스크린샷 2025-12-07 오전 1 02 15" src="https://github.com/user-attachments/assets/e0fff836-2a8e-46d2-846c-036661038332" />


### ❤️ 북마크 기능

* 상품 북마크 / 북마크 취소
* 로그인한 사용자에 대해서만 북마크 제공
* 북마크한 상품 상세조회 가능
<img width="1710" height="1107" alt="스크린샷 2025-12-07 오전 1 04 28" src="https://github.com/user-attachments/assets/5e2c9643-b6c5-4fc4-91c6-675a326a7e88" />


---

## 🛠 기술 스택

| 항목          | 내용                         |
| ----------- | -------------------------- |
| **언어**      | Python 3.x                 |
| **프레임워크**   | Flask                      |
| **데이터베이스**  | Firebase Realtime Database |
| **라이브러리**   | Flask, pyrebase4 등         |
| **개발 도구**   | VS Code, GitHub            |
| **UI 디자인**  | Figma                      |
| **협업**   | GitHub, Notion                |

---

## 📁 프로젝트 구조

```
EwhaMarket/
├── __pycache__/
├── .github/
│   └── (GitHub Actions / workflows 등)
│
├── authentication/
│   └── firebase_auth.json        # Firebase 서비스 계정 키
│
├── static/
│   ├── images/                   # 정적 이미지 파일
│   │
│   ├── index.css
│   ├── list.css
│   ├── main.js
│   ├── product_detail.css
│   ├── reg_items.css
│   ├── reg_reviews.css
│   ├── review_detail.css
│   ├── review.css
│   └── style.css                 # 공통 스타일
│
├── templates/
│   ├── index.html                # 네비게이션 바
│   ├── list.html                 # 상품 목록 조회
│   ├── login.html                # 로그인
│   ├── logout.html               # 로그아웃 
│   ├── product_detail.html       # 상품 상세 페이지
│   ├── reg_items.html            # 상품 등록
│   ├── reg_reviews.html          # 리뷰 작성
│   ├── review_detail.html        # 리뷰 상세
│   ├── review.html               # 리뷰 목록 조회
│   ├── signup.html               # 회원가입
│   └── wishlist.html             # 찜 목록 페이지
│
├── .gitignore
├── app.py                        # Flask 앱 실행 및 라우팅
├── database.py                   # Firebase 데이터 처리 로직
└── README.md

```

---

## 🔧 설치 및 실행 가이드
아래 기술 블로그에서 설치 및 실행 가이드를 확인하실 수 있습니다. 
```
https://amazing-stallion-b39.notion.site/2b7395a284608057a716df4518eee985?source=copy_link
```

---

## 👥 팀 구성 및 역할
###🎨 Frontend / 🧩 Backend 역할 표

| 구분 / 이름   | **명아령**                                                  | **조혜림**                                                      | **Amingoo Temuujin**                                     | **이유진**                                                  | **정윤아**                                                  |
| --------- | -------------------------------------------------------- | ------------------------------------------------------------ | -------------------------------------------------------- | -------------------------------------------------------- | -------------------------------------------------------- |
| **역할**    | Frontend                                                 | Frontend                                                     | Frontend                                                 | Backend                                                  | Backend                                                  |
| **상세 업무** | - 상품 등록 화면 개발<br>- 상품 전체 조회 / 상세 조회 UI                   | - 리뷰 작성 / 조회 / 상세 화면 개발<br>- 네비게이션 바 구현<br>- Flash 메시지 동작 처리 | - 회원가입 / 로그인 / 로그아웃 화면 개발                                | - 리뷰 등록 / 조회 기능<br>- 회원가입 / 로그인 / 로그아웃 기능                       | - 팀장<br>- 상품 등록 / 조회 기능<br>- 북마크(찜) 전체 기능 구현                     |

