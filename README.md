#  Learning Management System API

A fully functional, production-grade e-learning backend built with **FastAPI** and **PostgreSQL**. Deployed and live.

 **Live API Docs:** https://lms-api-3p9x.onrender.com/  
 **GitHub:** https://github.com/1-dara/lms-api

---

##  Features

- **JWT Authentication** — Secure register and login with access tokens
- **Role-Based Access Control** — Admin, Instructor, and Student roles
- **Course Management** — Full CRUD for courses
- **Lesson Management** — Create and manage lessons within courses
- **Student Enrollments** — Track which students are enrolled in which courses
- **Image Uploads** — Permanent cloud image storage via Cloudinary
- **Auto-generated Docs** — Interactive Swagger UI at `/docs`
- **Redis Caching** — Property listings and detail pages cached for 5 minutes, reducing database load on repeated requests


---

##  Tech Stack

| Technology | Purpose |
|---|---|
| FastAPI | Web framework |
| PostgreSQL | Database |
| SQLAlchemy (Async) | ORM |
| Alembic | Database migrations |
| JWT / OAuth2 | Authentication |
| bcrypt | Password hashing |
| Cloudinary | Image storage |
| Render | Deployment |
| Pydantic | Data validation |
| Redis | Caching layer for property/product/course listings |


---

##  Project Structure

```
lms_api/
├── app/
│   ├── main.py               # App entry point
│   ├── database.py           # PostgreSQL connection
│   ├── models/               # Database models
│   │   ├── user.py
│   │   ├── course.py
│   │   ├── lesson.py
│   │   ├── enrollment.py
│   │   └── image.py
│   ├── schemas/              # Pydantic validation schemas
│   ├── routers/              # API route handlers
│   │   ├── auth.py
│   │   ├── courses.py
│   │   ├── lessons.py
│   │   └── images.py
│   └── core/
│       ├── config.py         # Environment settings
│       └── security.py       # JWT & password hashing
├── alembic/                  # Database migrations
├── requirements.txt
├── Procfile
└── README.md
```

---

##  API Endpoints

### Auth
| Method | Endpoint | Description | Auth |
|---|---|---|---|
| POST | `/api/auth/register` | Register a new user | ❌ |
| POST | `/api/auth/login` | Login and get JWT token | ❌ |

### Courses
| Method | Endpoint | Description | Auth |
|---|---|---|---|
| GET | `/api/courses/` | Get all courses | ❌ |
| POST | `/api/courses/` | Create a course | ✅ Instructor/Admin |
| GET | `/api/courses/{id}` | Get a single course | ❌ |
| PUT | `/api/courses/{id}` | Update a course | ✅ Owner only |
| DELETE | `/api/courses/{id}` | Delete a course | ✅ Owner only |

### Lessons
| Method | Endpoint | Description | Auth |
|---|---|---|---|
| GET | `/api/lessons/` | Get all lessons | ❌ |
| POST | `/api/lessons/` | Create a lesson | ✅ Instructor/Admin |
| GET | `/api/lessons/{id}` | Get a single lesson | ❌ |
| PUT | `/api/lessons/{id}` | Update a lesson | ✅ Owner only |
| DELETE | `/api/lessons/{id}` | Delete a lesson | ✅ Owner only |

### Images
| Method | Endpoint | Description | Auth |
|---|---|---|---|
| POST | `/api/images/upload` | Upload an image | ✅ |

---

##  Setup & Installation

1. **Clone the repository**
```bash
git clone https://github.com/1-dara/lms-api.git
cd lms-api
```

2. **Create virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Create a `.env` file**
```env
DATABASE_URL=postgresql+asyncpg://username@localhost:5432/lms_db
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
REDIS_URL="your-redis-url"
```

5. **Run database migrations**
```bash
alembic upgrade head
```

6. **Start the server**
```bash
uvicorn app.main:app --reload
```

7. **Visit the API docs**
```
http://127.0.0.1:8000/docs
```

---

##  Author

**Irene Peter-Okon Idara**  
Backend Developer  
1ireneokon@gmail.com  
github.com/1-dara
