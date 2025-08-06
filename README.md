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

## 🚀 Deployment
Add your specific AWS Elastic Beanstalk or Docker deployment steps here.

Example (to be completed by you):
```bash
# Build Docker image
...

# Push to ECR
...

# Deploy to Elastic Beanstalk
...
```

---

## 🔐 .ENV Variables

```ini
DATABASE_URL=mysql+mysqlconnector://root:your_password@your_host:3306/your_db_name
```

---

## ✅ How to Run Locally
```bash
# Clone the repository
git clone https://github.com/your-username/library-management.git
cd library-management

# Create and activate virtual environment (optional)
python -m venv venv
source venv/bin/activate  # For Linux/Mac
venv\Scripts\activate     # For Windows

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn app.main:app --reload
```

## 🧪 Sample Endpoints

| Method | Endpoint                                 | Description         |
|--------|------------------------------------------|---------------------|
| POST   | `/users/`                                | Create a new user   |
| GET    | `/users/`                                | List all users      |
| POST   | `/books/`                                | Create a new book   |
| GET    | `/books/`                                | List all books      |
| POST   | `/books/{book_id}/borrow/{user_id}`      | Borrow a book       |
| POST   | `/books/{book_id}/return/{user_id}`      | Return a book       |

---

## CURLs

#### POST Create a new User
```bash
curl --location 'http://<URL>:<port>/users/' \
--header 'Content-Type: application/json' \
--data '{"name": "Alice"}'
```

#### GET List all User
```bash GET List all User
curl --location 'http://<URL>:<port>/users/'
```

#### POST Create a new Book
```bash POST Create a new Book
curl --location 'http://<URL>:<port>/books/' \
--header 'Content-Type: application/json' \
--data '{"title": "1984", "author": "George Orwell"}'
```

#### GET List all Books
```bash GET List all Books
curl --location 'http://<URL>:<port>/books/'
```

#### POST Borrow Book
```bash
curl --location --request POST 'http://<URL>:<port>/books/1/borrow/2'
```

#### POST Return Book
```bash
curl --location --request POST 'http://<URL>:<port>/books/1/return/2'
```

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


