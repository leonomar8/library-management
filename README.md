# 📚 Library Management System (Backend API)

A FastAPI-based backend service for managing a library's book lending system. It allows users to register, borrow, and return books, while enforcing borrowing limits and calculating overdue fines.

---

## 🎯 Objective

To build a robust and scalable backend service that demonstrates key **Cloud Engineering** and **Software Development** skills using modern technologies and best practices.

---

## 📝 Project Description

This project simulates a digital library system where users can:

- Register as library members
- Regster books
- Borrow available books (up to a defined limit)
- Return borrowed books and incur fines for overdue returns
- View all users and their borrowing status

It is structured using the **MVC (Model-View-Controller)** architecture and incorporates both development and operational tooling to reflect real-world deployment scenarios.

---

## ⚙️ Tech Stack

### 💻 Backend
- **Python 3**
- **FastAPI** – API framework
- **Pydantic** – Data validation
- **SQLAlchemy** – ORM (Object Relational Mapping)
- **MySQL** – Relational Database

### 🛠 Dev Tools
- **Docker** – Containerization
- **docker-compose** – Multi-service orchestration
- **Git** – Version control
- **Unit Testing (pytest)** – For validation of business logic

### ☁️ Cloud / Deployment (Planned)
- **AWS RDS** – Hosted MySQL database
- **AWS Elastic Beanstalk** – App deployment
- **Security Groups** – Network-level access control

---

## 🧠 Skills Demonstrated

### 👨‍💻 Development
- Object-Oriented Programming (OOP)
- MVC Project Architecture
- RESTful API Design
- SQLAlchemy ORM Models
- Pydantic Schema Validation
- Exception Handling & Error Messages
- Use of `lambda` functions for filtering and logic
- Modular Code Organization
- Unit & Integration Testing with `pytest`

### 🧑‍💼 DevOps / Cloud Engineering
- Dockerized Application with `docker-compose`
- `.env` for Secure Configs
- Deployment-ready for AWS:
  - Elastic Beanstalk (Application)
  - RDS (Database)
  - Security Group Management

---

## 📁 Project Structure

```bash
your_project/
│
├── app/
│   ├── crud/                # Business logic layer
│   ├── models/              # SQLAlchemy models
│   ├── routes/              # API endpoints
│   ├── schemas/             # Pydantic schemas
│   ├── config.py            # Configuration setup
│   ├── database.py          # DB connection and Base
│   └── main.py              # Application entry point
│
├── tests/                   # Unit and integration tests
│
├── .env                     # Environment variables (e.g. DB URL)
├── docker-compose.yml       # Multi-container orchestration
├── requirements.txt         # Python dependencies
├── .gitignore               # Git exclusions
└── README.md                # This file

