## 1. 📌 프로젝트 개요
### 📆 개발 기간

- **2025.06.15 ~ 2025.06.16 (2일)**
### 👤 개발 인원

- **1인 개인 프로젝트**

| 항목         | 내용                                                       |
| ---------- | -------------------------------------------------------- |
| **프로젝트 명** | 고객지원 질문·답변 게시판 (QnA Board)                               |
| **개요**     | 사용자가 질문을 등록하고, 관리자가 답변을 작성할 수 있는 QnA 게시판 웹 애플리케이션        |
| **개발 목적**  | Flask, Vue.js, MySQL을 활용한 실전 웹 프로젝트 구현 능력 향상 및 풀스택 구조 이해 |
| **주요 기술**  | Flask, Vue.js, MySQL, PyMySQL, REST API, JWT 인증          |
| **대상 사용자** | 일반 사용자, 게시판 관리자                                          |

---

## 2. 🧪 기술 요구사항

- **백엔드**
    - Python (Flask)
        - REST API 서버
        - Blueprint 기반 구조화
    - MySQL 8.0 (PyMySQL 사용)
- **프론트엔드**
    - Vue 3 (Vite + Composition API)
    - SCSS (Nesting), Bootstrap 기반 UI
    - 상태관리: Pinia
    - HTTP 통신: Axios
    - 라우터: vue-router
- **기타**
    - JWT 기반 인증/인가
    - CORS 설정
    - 비밀번호 bcrypt 암호화
    - 질문 목록 페이징 처리

---

## 3. 🧩 핵심 기능 요약

|분류|기능|설명|
|---|---|---|
|회원|회원가입|유효성 검사, 중복 ID/이메일 체크, 비밀번호 암호화 저장|
|〃|로그인 / 로그아웃|JWT 발급 및 해제|
|질문|질문 작성|로그인 사용자만 가능|
|〃|목록 조회|페이징, 정렬, 검색 포함|
|〃|상세 조회|질문 + 답변 목록|
|〃|수정 / 삭제|작성자 또는 관리자만 가능|
|답변|답변 작성|관리자만 가능|
|〃|수정|관리자만 가능|
|〃|삭제|관리자만 가능|
|마이페이지|내 질문 목록|로그인한 사용자 본인만 접근 가능|

---


## 4. 📂 데이터베이스 모델 설계

### 🔹 사용자 테이블 (`user`)

```sql
CREATE TABLE user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    login_id VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    is_admin TINYINT(1) DEFAULT 0,
    is_deleted TINYINT(1) DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

- bcrypt로 비밀번호 암호화
- 사용자 이름은 UI에선 '홍**' 형식으로 마스킹

### 🔹 문의 테이블 (`inquiry`)

```sql
CREATE TABLE inquiry (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    is_secret TINYINT(1) DEFAULT 0,
    is_deleted TINYINT(1) DEFAULT 0,
    status ENUM('open', 'answered', 'closed') DEFAULT 'open',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE
);
```

### 🔹 답변 테이블 (`answer`)

```sql
CREATE TABLE answer (
    id INT AUTO_INCREMENT PRIMARY KEY,
    inquiry_id INT,
    admin_id INT,
    content TEXT NOT NULL,
    is_deleted TINYINT(1) DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (inquiry_id) REFERENCES inquiry(id) ON DELETE SET NULL,
    FOREIGN KEY (admin_id) REFERENCES user(id) ON DELETE SET NULL
);
```

---

## 5. 📡 REST API 사양

> Base URL Prefix: /api

### 1) 사용자 API (`/api/users`)

|메서드|경로|설명|권한|
|---|---|---|---|
|POST|`/users`|회원가입|누구나|
|POST|`/login`|로그인|누구나|
|GET|`/users/:id`|회원정보 조회|본인 / 관리자|
|PUT|`/users/:id`|회원정보 수정|본인|
|DELETE|`/users/:id`|회원 논리 삭제|본인|

---

### 2) 문의 API (`/api/inquiries`)

|메서드|경로|설명|권한|
|---|---|---|---|
|POST|`/inquiries`|문의글 작성|로그인 사용자|
|GET|`/inquiries`|전체 목록 조회|관리자 (일반 사용자는 본인 글 필터링)|
|GET|`/inquiries/:id`|상세 조회|작성자 / 관리자|
|PUT|`/inquiries/:id`|수정|작성자|
|DELETE|`/inquiries/:id`|논리 삭제|작성자|

---

### 3) 답변 API (`/api/answers`)

|메서드|경로|설명|권한|
|---|---|---|---|
|POST|`/answers`|답변 작성|관리자|
|GET|`/answers?inquiry_id=1`|해당 문의의 답변 목록|관리자 / 작성자|
|GET|`/answers/:id`|답변 상세 조회|관리자 / 작성자|
|PUT|`/answers/:id`|수정|관리자|
|DELETE|`/answers/:id`|삭제|관리자|

---

## 6. 기타 정책

### 📌 비밀글 처리

- `is_secret = 1` 인 경우:
    - 목록에서는 제목만 노출
    - 상세 조회는 작성자 본인 또는 관리자만 허용

### 🗑️ 논리 삭제 처리

```sql
-- 실제 삭제 대신 is_deleted 플래그만 설정
UPDATE [테이블명] SET is_deleted = 1 WHERE id = :id;
```

- 데이터 조회 시 항상 `WHERE is_deleted = 0` 조건 필수

### 🔐 인증/인가 방식

- JWT 토큰 방식
- 로그인 성공 시 토큰 발급 후 클라이언트 저장
- 요청 시 Authorization 헤더에 포함
- `is_admin = 1` 로 관리자 여부 판별

---
## 피드백

### 1. 백엔드에서 로깅 필요 (에러 메세지 로깅)

- logging 모듈 쓰기
- 로깅을 위한 코드 필요
- 서버 실행 중 발생한 에러 내용을 자동으로 저장하는 기능과 저장하는 파일이 있어야 한다.

### 2. sql은 스네이크 케이스, js는 카멜 케이스 표기

- Spring JPA처럼 DB에서 데이터를 불러와 매핑할 때 자동으로 변수 이름을 카멜케이스로 바꾸지 않는다.
    - created_at(sql 컬럼이름) → createdAt으로 자동 변환
- 프론트를 위해서 response 날리기 전(보통 직전이 괜찮음) 카멜 케이스로 변환해서 보내야 한다.

### 3. 파일 구조 (좋지 못함)

```bash
backend/
├── app/                        # 주요 애플리케이션 코드
│   ├── __init__.py             # Flask 앱 초기화 및 확장 등록
│   ├── config.py               # 환경 설정 (DB, JWT 시크릿 등)
│
│   ├── models/                 # 데이터베이스 모델 정의
│   │   ├── __init__.py
│   │   ├── user_model.py
│   │   ├── inquiry_model.py
│   │   └── answer_model.py
│
│   ├── routes/                 # API 라우팅
│   │   ├── __init__.py
│   │   ├── user_routes.py
│   │   ├── inquiry_routes.py
│   │   └── answer_routes.py
│
│   ├── services/               # 비즈니스 로직 처리
│   │   ├── user_service.py
│   │   ├── inquiry_service.py
│   │   └── answer_service.py
│
│   └── utils/                  # 유틸리티 (JWT 등)
│       └── jwt_util.py
│
├── run.py                      # 앱 실행 엔트리포인트
└── requirements.txt            # 의존성 패키지 목록
```

- 모델, 라우트, 서비스로 나누지 말고 user, inquiry, answer 별(기능)로 폴더를 나눠야 한다.

```bash
app/
├── user/
│   ├── user_model.py         # DB 모델
│   ├── user_routes.py        # Flask Blueprint 라우트
│   ├── user_service.py       # 비즈니스 로직
│   └── __init__.py           # 모듈 초기화용 (선택)
│
├── inquiry/
│   ├── inquiry_model.py
│   ├── inquiry_routes.py
│   ├── inquiry_service.py
│   └── __init__.py
│
├── answer/
│   ├── answer_model.py
│   ├── answer_routes.py
│   ├── answer_service.py
│   └── __init__.py
│
├── utils/                    # 공통 유틸 함수
│   ├── jwt_util.py
│   ├── password_util.py
│   ├── error_handler.py
│   └── __init__.py
│
├── config.py                # 환경설정 (DB, JWT, etc)
├── db.py                    # DB 연결, 초기화
└── __init__.py              # create_app 함수 등
```