## ✅ 사용자 API

### 🔐 로그인

- **POST** `/api/login`
- JWT 필요: ❌
- 관리자 전용: ❌
- 요청:

```json
{
  "login_id": "user123",
  "password": "1234abcd"
}
```

- 응답:

```json
{
  "token": "<JWT Token>"
}
```

---

### 📝 회원가입

- **POST** `/api/users`
- JWT 필요: ❌
- 관리자 전용: ❌
- 요청:

```json
{
  "login_id": "user123",
  "password": "1234abcd",
  "name": "홍길동",
  "email": "user@example.com"
}
```

- 응답:

```json
{
  "success": true,
  "response": {
    "id": 1,
    "login_id": "user123",
    "name": "홍길동"
  },
  "status": 201,
  "errorMessage": null
}
```

---

### ❌ 회원 탈퇴

- **DELETE** `/api/users`
- JWT 필요: ✅
- 관리자 전용: ❌
- 요청:

```json
{
  "login_id": "user123",
  "password": "1234abcd"
}
```

- 응답:

```json
{
  "success": true,
  "response": {
    "message": "회원 탈퇴가 완료되었습니다."
  },
  "status": 200,
  "errorMessage": null
}
```

---

### ✏️ 회원정보 수정

- **PUT** `/api/users/<user_id>`
- JWT 필요: ✅
- 관리자 전용: ❌
- 요청:

```json
{
  "login_id": "user123",
  "password": "1234abcd",
  "new_name": "김길동",
  "new_email": "new@example.com",
  "new_password": "newpass123"
}
```

- 응답:

```json
{
  "success": true,
  "response": {
    "message": "회원정보가 수정되었습니다."
  },
  "status": 200,
  "errorMessage": null
}
```

---

### 👤 마이페이지 조회

- **GET** `/api/users/<user_id>`
- JWT 필요: ✅
- 관리자 전용: ❌
- 요청: 없음
- 응답:

```json
{
  "success": true,
  "response": {
    "id": 1,
    "login_id": "user123",
    "name": "김길동",
    "email": "new@example.com",
    "is_admin": false,
    "created_at": "2025-06-13 10:00:00"
  },
  "status": 200,
  "errorMessage": null
}
```

---

## ✅ 문의글 API

### 📝 문의글 등록

- **POST** `/api/inquiries`
- JWT 필요: ✅
- 관리자 전용: ❌
- 요청:

```json
{
  "user_id": 1,
  "title": "로그인 오류",
  "content": "로그인이 안 됩니다.",
  "is_secret": 0
}
```

- 응답:

```json
{
  "success": true,
  "response": {
    "message": "문의글이 등록되었습니다."
  },
  "status": 201,
  "errorMessage": null
}
```

---

### 📋 전체/필터 조회

- **GET** `/api/inquiries?keyword=로그인&page=1&size=10&sort=latest`
- JWT 필요: ✅
- 관리자 전용: ❌
- 요청: 없음
- 응답:

```json
{
  "success": true,
  "response": [
    {
      "id": 1,
      "title": "로그인 오류",
      "user_id": 1,
      "status": "waiting",
      "created_at": "2025-06-13"
    }
  ],
  "status": 200,
  "errorMessage": null
}
```

---

### 🔍 단일 문의글 조회

- **GET** `/api/inquiries/<id>`
- JWT 필요: ✅
- 관리자 전용: ❌
- 요청: 없음
- 응답:

```json
{
  "success": true,
  "response": {
    "id": 1,
    "title": "로그인 오류",
    "content": "로그인이 안 됩니다.",
    "user_id": 1,
    "status": "waiting",
    "created_at": "2025-06-13"
  },
  "status": 200,
  "errorMessage": null
}
```

---

### ✏️ 문의글 수정

- **PUT** `/api/inquiries/<id>`
- JWT 필요: ✅
- 관리자 전용: ❌
- 요청:

```json
{
  "title": "비밀번호 변경",
  "content": "비밀번호 변경이 필요합니다.",
  "is_secret": 1
}
```

- 응답:

```json
{
  "success": true,
  "response": {
    "message": "문의글이 수정되었습니다."
  },
  "status": 200,
  "errorMessage": null
}
```

---

### ❌ 문의글 삭제

- **DELETE** `/api/inquiries/<id>`
- JWT 필요: ✅
- 관리자 전용: ❌
- 요청: 없음
- 응답:

```json
{
  "success": true,
  "response": {
    "message": "문의글이 삭제되었습니다."
  },
  "status": 200,
  "errorMessage": null
}
```

---

## ✅ 답변 API

### 📝 답변 등록

- **POST** `/api/answers`
- JWT 필요: ✅
- 관리자 전용: ✅
- 요청:

```json
{
  "inquiry_id": 1,
  "admin_id": 99,
  "content": "문의 확인 후 처리했습니다."
}
```

- 응답:

```json
{
  "success": true,
  "response": {
    "message": "답변이 등록되었습니다."
  },
  "status": 201,
  "errorMessage": null
}
```

---

### 🔍 단일 답변 조회

- **GET** `/api/answers/<id>`
- JWT 필요: ✅
- 관리자 전용: ❌
- 요청: 없음
- 응답:

```json
{
  "success": true,
  "response": {
    "id": 1,
    "inquiry_id": 1,
    "admin_id": 99,
    "content": "문의 확인 후 처리했습니다.",
    "admin_name": "관리자",
    "created_at": "2025-06-13"
  },
  "status": 200,
  "errorMessage": null
}
```

---

### 📋 문의별 답변 목록

- **GET** `/api/answers?inquiry_id=1`
- JWT 필요: ✅
- 관리자 전용: ❌
- 요청: 없음
- 응답:

```json
{
  "success": true,
  "response": [
    {
      "id": 1,
      "inquiry_id": 1,
      "admin_id": 99,
      "content": "문의 확인 후 처리했습니다.",
      "admin_name": "관리자",
      "created_at": "2025-06-13"
    }
  ],
  "status": 200,
  "errorMessage": null
}
```

---

### ✏️ 답변 수정

- **PUT** `/api/answers/<id>`
- JWT 필요: ✅
- 관리자 전용: ✅
- 요청:

```json
{
  "content": "답변 내용을 수정했습니다."
}
```

- 응답:

```json
{
  "success": true,
  "response": {
    "message": "답변이 수정되었습니다."
  },
  "status": 200,
  "errorMessage": null
}
```

---

### ❌ 답변 삭제

- **DELETE** `/api/answers/<id>`
- JWT 필요: ✅
- 관리자 전용: ✅
- 요청: 없음
- 응답:

```json
{
  "success": true,
  "response": {
    "message": "답변이 삭제되었습니다."
  },
  "status": 200,
  "errorMessage": null
}
```

