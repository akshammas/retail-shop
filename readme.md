# Retail Shop API

A production-grade FastAPI e-commerce backend built over 27 days.

## Phase 1 Complete ✅

### Stack
- Python 3.14
- FastAPI
- Pydantic V2
- JWT Authentication (python-jose)
- Password Hashing (bcrypt)
- pytest (98% coverage)

## Project Structure

retail-shop/
├── main.py
├── requirements.txt
├── .env (not committed)
├── app/
│   ├── core/
│   │   ├── config.py       ← environment settings
│   │   └── security.py     ← JWT + bcrypt
│   ├── routers/
│   │   ├── auth.py         ← signup, login, refresh, logout
│   │   ├── products.py     ← full CRUD with admin controls
│   │   ├── users.py        ← profile, update, delete
│   │   └── orders.py       ← coming in Phase 2
│   ├── schemas/
│   │   ├── product.py      ← Pydantic models
│   │   └── user.py         ← Pydantic models
│   ├── dependencies.py     ← get_current_user, require_admin
│   └── database.py         ← in-memory fake db (Phase 2 → PostgreSQL)
└── tests/
    ├── conftest.py
    ├── test_auth.py
    ├── test_products.py
    ├── test_users.py
    ├── test_orders.py
    └── test_admin.py

## Run Locally

pip install -r requirements.txt
uvicorn main:app --reload

## API Docs
Visit http://localhost:8000/docs

## Auth Routes
| Method | Route | Access |
|--------|-------|--------|
| POST | /auth/signup | Public |
| POST | /auth/login | Public |
| POST | /auth/refresh | Public |
| POST | /auth/logout | Protected |
| GET | /auth/me | Protected |

## Product Routes
| Method | Route | Access |
|--------|-------|--------|
| GET | /products/ | Public |
| GET | /products/{id} | Public |
| GET | /products/featured | Public |
| POST | /products/ | Admin |
| PUT | /products/{id} | Admin |
| DELETE | /products/{id} | Admin |

## User Routes
| Method | Route | Access |
|--------|-------|--------|
| GET | /users/me/profile | Protected |
| PUT | /users/me/update | Protected |
| DELETE | /users/me/delete | Protected |
| GET | /users/ | Admin |
| DELETE | /users/{id} | Admin |

## Test Results
67 tests passing
98% coverage

## Coming in Phase 2
- PostgreSQL + SQLAlchemy
- Alembic migrations
- Orders + Cart system
- Payment integration (Razorpay)
- Image uploads
- Email verification
- Rate limiting
- Redis caching
- Docker deployment