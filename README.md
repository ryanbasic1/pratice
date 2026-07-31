<div align="center">

# 🌌 Untold Backend

### Production-ready backend powering **Untold** — an anonymous social platform where every thought deserves a home.

<p align="center">
<img src="https://img.shields.io/badge/FastAPI-0FA36B?style=for-the-badge&logo=fastapi&logoColor=white"/>
<img src="https://img.shields.io/badge/PostgreSQL-336791?style=for-the-badge&logo=postgresql&logoColor=white"/>
<img src="https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge"/>
<img src="https://img.shields.io/badge/Alembic-222222?style=for-the-badge"/>
<img src="https://img.shields.io/badge/JWT-000000?style=for-the-badge"/>
<img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker"/>
</p>

<p align="center">
Anonymous • Secure • Scalable • Open Source
</p>

</div>

---

## ✨ Overview

**Untold** is an anonymous social platform built around one simple idea:

> **Every thought deserves a home.**

Unlike traditional social media, Untold focuses on **ideas instead of identities**. Users can anonymously share thoughts, confessions, stories, dreams, and opinions in a safe, community-driven environment.

This repository contains the **backend service** responsible for authentication, APIs, database management, content interactions, and platform security.

---

# 🚀 Features

- 🔐 JWT Authentication
- 👤 Anonymous User Profiles
- 📝 Create, Update & Delete Thoughts
- ❤️ Like / Unlike Posts
- 🔍 Explore Community Feed
- 📄 User Dashboard
- ⚡ Optimized SQLAlchemy Queries
- 🛡 Secure Password Hashing
- 📦 RESTful API Architecture
- 🗄 PostgreSQL Database
- 🔄 Alembic Database Migrations

---

# 🏗 Tech Stack

| Category | Technology |
|----------|------------|
| Backend | FastAPI |
| ORM | SQLAlchemy |
| Database | PostgreSQL |
| Authentication | JWT |
| Password Hashing | pwdlib (Argon2) |
| Migrations | Alembic |
| Validation | Pydantic |
| API Docs | Swagger / OpenAPI |
| Deployment | Docker (Planned) |

---

# 📂 Project Structure

```text
app/
│
├── auth/
├── database/
├── models/
├── routers/
├── schemas/
├── services/
├── utils/
├── dependencies/
├── migrations/
└── main.py
```

---

# 🛠 Getting Started

### Clone Repository

```bash
git clone https://github.com/ryanbasic1/pratice.git
cd pratice
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment

Create a `.env` file:

```env
DATABASE_URL=postgresql://username:password@localhost/untold
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Run

```bash
uvicorn app.main:app --reload
```

Swagger UI

```
http://localhost:8000/docs
```

---

# 🗃 Database Design

Current core entities:

- Users
- Thoughts
- Likes

Planned production schema:

- Comments
- Reactions
- Bookmarks
- Notifications
- Reports
- Topics
- Media
- Sessions
- Refresh Tokens
- Activity Logs

---

# 🔒 Security

- JWT Authentication
- Argon2 Password Hashing
- Protected Routes
- Ownership Validation
- Input Validation
- SQL Injection Protection (ORM)
- Environment-based Secrets

---

# 📈 Roadmap

- [ ] Redis Caching
- [ ] WebSocket Notifications
- [ ] Comments & Replies
- [ ] Full-Text Search
- [ ] Trending Feed Algorithm
- [ ] Background Workers
- [ ] Media Uploads
- [ ] Rate Limiting
- [ ] Refresh Tokens
- [ ] Docker Compose
- [ ] CI/CD Pipeline
- [ ] Unit & Integration Tests

---

# 🤝 Contributing

Contributions are welcome!

If you'd like to improve Untold:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Open a Pull Request

Please open an issue first if you're planning a major feature.

---

# ⭐ Support

If you find this project useful:

- ⭐ Star the repository
- 🐞 Report bugs
- 💡 Suggest new features
- 🍴 Fork and contribute

---

# 📄 License

This project is licensed under the MIT License.

---

<div align="center">

**Built and thought by ARYAN using FastAPI & PostgreSQL**

*"Every thought deserves a home."*

</div>
