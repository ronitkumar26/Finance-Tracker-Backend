# Finance Tracker Backend

## Overview

This project is a **Finance Tracker Backend API** built using **FastAPI, SQLAlchemy, and PostgreSQL**. The system allows users to manage financial records such as **income and expenses**, generate **financial summaries**, and enforce **role-based access control**.

The goal of this project is to demonstrate backend development skills including:

* REST API design
* Database modeling
* Data filtering and pagination
* Role-based access control
* Financial analytics logic
* Input validation and error handling

---

# Tech Stack

* **Python**
* **FastAPI**
* **SQLAlchemy ORM**
* **PostgreSQL**
* **JWT Authentication**
* **Pydantic for validation**
* **Uvicorn**

---

# Project Structure

```
Finance-Tracker-Backend/
├── app/
│   ├── main.py              # Application entry point
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py        # Environment & App configurations
│   │   ├── oauth2.py        # Token handling & authentication
│   │   └── security.py      # Password hashing & JWT logic
│   ├── database/
│   │   └── db.py            # Database engine & session configuration
│   ├── models/
│   │   ├── __init__.py
│   │   ├── transaction.py   # SQLAlchemy transaction models
│   │   └── users.py         # SQLAlchemy user models
│   ├── routes/
│   │   ├── auth.py          # Authentication/Login routes
│   │   ├── summary.py       # Financial summary & stats routes
│   │   ├── transaction.py   # Transaction CRUD routes
│   │   └── users.py         # User management routes
│   └── schemas/
│       ├── __init__.py
│       ├── transaction.py   # Pydantic models for transactions
│       └── users.py         # Pydantic models for users
│   
├── alembic/                 # Database migrations
├── .env                     # Environment secrets (not to be committed)
├── .gitignore
├── alembic.ini
├── requirements.txt
└── README.md
```

# Features

## 1 Financial Records Management

The system allows storing and managing financial transactions.

Each transaction contains:

* Amount
* Type (Income / Expense)
* Category
* Date
* Notes
* User ID

### CRUD Operations

Users can:

* Create transactions
* View transactions
* Update transactions
* Delete transactions

---

## 2 Filtering Transactions

Transactions can be filtered using query parameters:

* Category
* Type
* Start date
* End date

Example:

```
GET /transactions?category=food&type=expense
```

---

## 3 Pagination

To handle large datasets, pagination is implemented.

Example:

```
GET /transactions?skip=0&limit=10
```

* **skip** → number of records to skip
* **limit** → number of records returned

---

# 4 Financial Summary and Analytics

The backend provides financial insights through summary endpoints.

### Available summaries

* Total Income
* Total Expenses
* Current Balance
* Category-wise breakdown
* Monthly totals
* Recent transactions

Example endpoints:

```
GET /summary/total-income
GET /summary/total-expenses
GET /summary/balance
GET /summary/category-breakdown
GET /summary/monthly-summary
GET /summary/recent
```

These endpoints process financial records and return meaningful analytics.

---

# 5 User and Role Management

The system supports **basic user management** with three roles.

### Roles

**Viewer**

* Can view transactions
* Can view summaries

**Analyst**

* Can view transactions
* Can filter records
* Can access detailed summaries

**Admin**

* Full access
* Create users
* Update users
* Delete users
* Create transactions
* Update transactions
* Delete transactions

Role-based permissions are enforced using **FastAPI dependencies**.

---

# 6 Authentication

Authentication is implemented using **JWT tokens**.

Users login using:

```
POST /login
```

The system returns an **access token** which must be used for protected routes.

Example header:

```
Authorization: Bearer <token>
```

Passwords are **securely hashed before storing in the database**.

---

# 7 Validation and Error Handling

The system includes:

* Input validation using **Pydantic**
* Proper error responses
* HTTP status codes
* Clear error messages

Examples:

* 400 → Bad request
* 401 → Unauthorized
* 403 → Forbidden
* 404 → Not found

---

# Running the Project

### 1 Install dependencies

```
pip install -r requirements.txt
```

### 2 Run the server

```
uvicorn app.main:app --reload
```

Server will start at:

```
http://127.0.0.1:8000
```

---

# API Documentation

FastAPI automatically generates API documentation.

Swagger UI:

```
http://127.0.0.1:8000/docs
```


# Example Transaction

```
{
  "user_id": 5,
  "amount": 50000,
  "type": "income",
  "category": "salary",
  "date": "2026-04-01",
  "note": "Monthly salary"
}
```

---

# Key Design Decisions

* Separation of concerns using **routes, models, schemas, and core logic**
* Role-based access control using **dependency injection**
* Query-based filtering instead of separate endpoints
* Pagination for better performance
* Clear API structure for easy testing

---

# Future Improvements

Possible enhancements include:

* Admin dashboard
* CSV import/export
* Unit tests
* Advanced analytics
* Budget tracking
* Graph-based financial insights

---

# Conclusion

This project demonstrates a structured backend system capable of managing financial data, applying role-based access control, generating analytics, and maintaining clean API design using modern Python frameworks.

---
