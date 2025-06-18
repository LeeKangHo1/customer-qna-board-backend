## 1. 📌 프로젝트 개요

|항목|내용|
|---|---|
|**프로젝트 명**|고객지원 질문·답변 게시판 (QnA Board)|
|**개요**|사용자가 질문을 등록하고, 관리자가 답변을 작성할 수 있는 QnA 게시판 웹 애플리케이션|
|**개발 목적**|Flask, Vue.js, MySQL을 활용한 실전 웹 프로젝트 구현 능력 향상 및 풀스택 구조 이해|
|**주요 기술**|Flask, Vue.js, MySQL, PyMySQL, REST API, JWT 인증|
|**대상 사용자**|일반 사용자, 게시판 관리자|

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

## 4. 🔄 사용자 흐름

### 🔸 1단계: 회원가입

- 사용자는 회원가입 페이지에서 `login_id`, `비밀번호`, `이름`, `이메일`을 입력하여 가입 요청을 보냄
- 서버는 다음 작업을 수행:
    - `login_id`, `이메일` 중복 여부 확인
    - 이메일 형식 등 유효성 검사
    - 비밀번호를 bcrypt로 암호화하여 저장
- 회원가입 성공 시 `회원 고유번호(id)`가 발급되고, 로그인 가능 상태가 됨

---

### 🔸 2단계: 로그인

- 사용자가 로그인 페이지에서 `login_id`와 `비밀번호` 입력
- 서버는 다음 작업을 수행:
    - `login_id`에 해당하는 사용자 조회
    - bcrypt로 암호화된 비밀번호와 입력 비밀번호 비교
    - 일치할 경우 JWT 토큰을 생성하여 반환
- 클라이언트는 이 토큰을 브라우저에 저장하고, 이후 요청 시 `Authorization` 헤더에 포함시킴

---

### 🔸 3단계: 문의 목록 조회

- 로그인 사용자는 자신의 문의글 목록을 조회할 수 있음
- 관리자는 모든 사용자의 문의글 목록을 페이징 처리하여 조회 가능
- 문의글은 기본적으로 제목만 노출되며, `비밀글(is_secret=1)`은 권한이 없으면 제목 외 비공개 처리
- 목록 조회 시 다음과 같은 기능 포함:
    - 페이징 (page, size)
    - 정렬 옵션 (최신순, 답변 여부 등)
    - 키워드 검색 (제목, 내용 기준)

---

### 🔸 4단계: 문의글 상세 조회

- 목록에서 글을 클릭하면 해당 문의글 상세 정보 조회
- 서버는 다음 정보를 반환:
    - 제목, 내용, 작성자, 등록일시, 수정일시
    - 해당 글에 연결된 답변 목록
- 단, 비밀글인 경우 작성자 본인 또는 관리자인지 여부 검증 후에만 응답
- 삭제된 글(`is_deleted = 1`)은 조회 불가

---

### 🔸 5단계: 문의글 작성

- 로그인한 일반 사용자는 `문의 제목`, `문의 내용`, `비밀글 여부`를 입력하여 문의글 작성 가능
- 서버는 작성자의 `user_id`와 함께 `inquiry` 테이블에 저장
- 작성 후 목록으로 리디렉션되며 새 글이 반영됨

---

### 🔸 6단계: 답변 작성 (관리자 전용)

- 관리자는 문의글 상세 페이지에서 답변 등록 가능
- 답변 입력 시 `inquiry_id`, `admin_id`, `content`를 포함한 POST 요청 전송
- 서버는 해당 문의글 상태를 `'answered'`로 변경하고 `answer` 테이블에 레코드 추가

---

### 🔸 7단계: 사용자 답변 확인

- 사용자는 자신이 작성한 문의글에 답변이 달리면 상세 페이지에서 확인 가능
- `답변이 등록되었는지 여부`는 목록에서도 상태(status: open → answered)로 확인 가능
- 답변이 존재하면 함께 출력, 없으면 "답변 대기 중"으로 표시

---

### 🔸 8단계: 수정 / 삭제

- 문의글:
    - 작성자 본인만 수정 또는 삭제 가능 (`PUT`, `DELETE`)
    - 삭제 시 논리 삭제(`is_deleted = 1`) 처리
- 답변:
    - 관리자만 수정 / 삭제 가능
    - 삭제해도 문의글은 유지되며 답변만 사라짐

---

### 🔸 9단계: 마이페이지 접근

- 로그인한 사용자는 마이페이지에서 본인의 문의글 목록을 별도로 조회 가능
- 이 목록은 일반 목록과 동일하게 페이징, 정렬, 상태 표시 기능 포함

---

## 5. 📂 데이터베이스 모델 설계

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

## 6. 📡 REST API 사양

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

## 7. 기타 정책

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

## 8. 화면 페이지별 상세 설계

### 와이어프레임

### 1)🧍 회원가입 페이지 (`/register`)

**기능:** 로그인 ID, 비밀번호, 이름, 이메일 입력 → 가입

**필수 UI 요소:**

- `Input`: 로그인 ID
- `Input`: 비밀번호 (조건 안내, 비밀번호 확인 입력 포함)
- `Input`: 이름
- `Input`: 이메일
- `Button`: 회원가입
- `Alert`: 중복 여부 및 유효성 메시지
- ✅ 유효성 검사: 형식 체크 및 중복 체크 API 호출

---

### 2) 🔐 로그인 페이지 (`/login`)

**기능:** 로그인 ID / 비밀번호 입력 → JWT 토큰 발급

**필수 UI 요소:**

- `Input`: 로그인 ID
- `Input`: 비밀번호
- `Button`: 로그인
- `Link`: 회원가입 페이지 이동
- `Alert`: 로그인 실패 메시지

---

### 3) 🏠 QnA 목록 페이지 (`/inquiries`)

**기능:** 전체 문의글 조회 + 검색/정렬/페이징

**권한:** 관리자 → 전체 / 일반 사용자 → 본인 문의글만

**UI 요소:**

- `SearchBar`: 키워드 검색 (제목/내용)
- `Dropdown`: 정렬 옵션 (최신순, 답변여부)
- `List`: 문의글 목록 (제목, 작성일, 상태, 비밀글 여부 아이콘)
- `Pagination`: 페이지 이동
- `Button`: 문의글 작성 (로그인 시만 노출)

---

### 4) 📝 문의글 작성 페이지 (`/inquiries/write`)

**기능:** 제목 / 내용 / 비밀글 여부 작성

**UI 요소:**

- `Input`: 제목
- `Textarea`: 내용
- `Checkbox`: 비밀글 설정
- `Button`: 등록 / 취소

---

### 5) 📄 문의글 상세 페이지 (`/inquiries/:id`)

**기능:** 문의글 + 답변 조회, 수정/삭제 가능

**UI 요소:**

- `Card`: 문의글 정보 (작성자 이름 마스킹, 내용, 상태, 등록일)
- `Card`: 답변 정보 (있을 경우만)
- `Button`: 문의글 수정 / 삭제 (작성자 또는 관리자만)
- `Button`: 답변 등록 / 수정 / 삭제 (관리자만)

---

### 6) 💬 답변 작성/수정 폼 (컴포넌트)

**기능:** 텍스트 입력 후 등록/수정

**UI 요소:**

- `Textarea`: 답변 내용
- `Button`: 등록 / 수정

---

### 7) 👤 마이페이지 (`/mypage`)

**기능:** 로그인 사용자의 내 문의글 목록

**UI 요소:**

- `List`: 본인이 작성한 문의글 목록 (제목, 날짜, 상태)
- `Pagination`: 페이지 이동
- `Button`: 상세 보기 이동

---

## 🧱 공통 컴포넌트 설계

|컴포넌트명|설명|
|---|---|
|`Navbar.vue`|로그인/회원가입, 로그아웃, 마이페이지 링크 표시|
|`InquiryList.vue`|문의글 목록 리스트 전용 컴포넌트|
|`AnswerBox.vue`|답변 표시 컴포넌트|
|`AuthGuard.vue`|인증된 사용자만 접근 가능한 라우팅 처리|
|`Alert.vue`|에러/성공 메시지 표시용 컴포넌트|
|`Pagination.vue`|페이징 컴포넌트|
|`SearchBar.vue`|검색 키워드 입력 UI 컴포넌트|
|`SortDropdown.vue`|정렬 드롭다운 UI 컴포넌트|

---

## 🧭 화면 흐름 예시 (비밀글 포함)

- 목록에서 `🔒 비밀글` 클릭
    
    → 작성자 또는 관리자면 상세 열람 가능
    
    → 아니라면 `권한 없음` 메시지 표시
    

---
