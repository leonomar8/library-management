# Library Management System (Backend API)
A Python FastAPI-based backend service for managing a library's book lending system. It allow to add books to the library, users to register, borrow, and return books, while enforcing borrowing limits and calculating overdue fines.


![Alt text](diagram.png)



## 1. Objective
To build a robust and scalable backend service that demonstrates **Cloud Engineering** and **OOP Software Development** skills using modern technologies and best practices.

## 2. Project Description
This project simulates a digital library system where users can:

- Register as library members
- Borrow available books (up to a defined limit)
- Return borrowed books and incur fines for overdue returns
- View all users and their borrowing status
- The system also has an API to add books to the library

It is structured using the **MVC (Model-View-Controller)** architecture and incorporates both development and operational tooling to reflect real-world deployment scenarios.


## 3. Tech Stack

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
- **AWS Elastic Beanstalk** – App deployment by console and CLI
- **Security Groups** – Network-level access control


## 4. Skills Demonstrated

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
- Dockerized DB with `docker-compose` for local testing
- `.env` for Secure Configs
- Deployment-ready for AWS:
  - Elastic Beanstalk (EBS)
  - Configure Procfile and application.py to prepare the project for EBS deployment.
  - Fast deployment by using AWS CLI and EBS CLI
  - RDS DB
  - Security Group Management


## 5. Deployment

### Run Locally
```bash
# Clone the repository
git clone https://github.com/your-username/library-management.git
cd library-management

# Create and activate virtual environment (optional)
python -m venv venv
source venv/bin/activate  # For Linux/Mac
venv\Scripts\activate     # For Windows

# Run a MySQL docker container
nano docker-compose.yml    # Check script below
docker-compose up -d

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn app.main:app --reload
```

.ENV

```ini
DATABASE_URL=mysql+mysqlconnector://root:your_password@your_host:3306/your_db_name
```

MySQL Docker Compose Script
```ini
version: '3.8'
services:
  mysql:
    image: mysql:8
    container_name: mysql_fastapi
    restart: always
    environment:
      MYSQL_DATABASE: mydb
      MYSQL_ROOT_PASSWORD: 12345
      MYSQL_USER: omar
      MYSQL_PASSWORD: pass
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql

volumes:
  mysql_data:
```
  
### Elastic Beanstalk (GUI) + RDS

Prepare the project to deploy in EBS using the AWS Console
```init
# Files added for EBS deployment:
  - application.py: The spected entry pont for EBS is application.py. No need to change main.py
  - Procfile: EBS expects a WSGI-compatible interface, but FastAPI is ASGI-based. To bridge this, use Gunicorn with the Uvicorn worker to serve FastAPI properly.

# Files updated for EBS deployment:
  - requirements.txt: Add gunicorn
  
# ZIP these files of the project
	- app/, application.py, Procfile, requirements.txt

# Spin up an RDS DB with these config:
  - Be aware of region, VPC and AZ, you'll use the same for EBS
  - Private Access
  - SG with port 3306 open
  - Relevant values to connect EBS with RDS:
    - Master username: root
    - Master password: ******8
    - Initial database name: mydb
  - Once RDS is active, copy the connection endpoint

# EBS doesn't use .env file, instead you add env variables by console
```

Steps to config EBS by Console
```init
# AWS > Elastic Beanstalk > Create Application
	- Step 1: Configure environment:
		- Environment tier: Web server environment
		- Application name: lib-mgmt
		- Environment name: lib-mgmt-dev
		- Platform: Python
		- Platform branch: Python 3.13
		- Platform version: 4.7.0 (Recommended)
		- Version label: v1
		- Upload application: upload your ZIP file
		- Configuration presets: Single instance
	- Step 2: Configure service access
		- Service role: aws-elasticbeanstalk-service-role
			# This role is created with this parameters in AWS > IAM > Roles > Create Role:
			- Trusted entity type: AWS Service
			- Service or use case: Elastic Beanstalk
			- Use case: Elastic Beanstalk - Environment
			- Add Permissions:
				- AWSElasticBeanstalkManagedUpdatesCustomerRolePolicy
				- AWSElasticBeanstalkEnhancedHealth
			- Role name: aws-elasticbeanstalk-service-role
		- EC2 instance profile: aws-elasticbeanstalk-ec2-role
			# This role is created with this parameters in AWS > IAM > Roles > Create Role:
			- Trusted entity type: AWS Service
			- Service or use case: Elastic Beanstalk
			- Use case: Elastic Beanstalk - Compute
			- Add Permissions:
				- AWSElasticBeanstalkMulticontainerDocker
				- AWSElasticBeanstalkWebTier
				- AWSElasticBeanstalkWorkerTier
		 	- Role name: aws-elasticbeanstalk-ec2-role
	- Step 3: Set up networking, database
		- VPC: Default
		- subnets: us-east-1a
	- Step 4: Configure instance traffic and scaling
		- EC2 security groups: SG with port 80 open
	- Step 5: Configure updates, monitoring, and logging
		- Environment properties:
			DATABASE_URL: mysql+mysqlconnector://root:password@<DB_URL>:3306/mydb

# Note forStep 2: EC2 connects to RDS via network access—no IAM permissions needed. However, a direct connection to RDS requires "AmazonRDSFullAccess" IAM permissions.
```

### Elastic Beanstalk (CLI) + RDS

Deploy project programmatically in EBS with AWS CLI and EBS CLI
```bash
# Check that AWS CLI and EBS CLI are installed
	$ aws --version
	$ eb --version

# Enter AWS credentials
	$ aws configure					
		AWS Access Key
		Secret Key
		Region (us-east-1)
	$ aws sts get-caller-identity		# check credentials are ok
	
# Clone project repo
	$ git clone https://github.com/username/library-management.git
	$ cd library-management
	$ python3 -m venv venv					# Python venv
	$ source venv/bin/activate				# Python venv

# Initialize EB Project
	$ eb init -p python-3.13 lib-mgmt --region us-east-1			# EB App name "lib-mgmt"
	$ eb create lib-mgmt-dev --single								# creates an environment
	$ eb use lib-mgmt-dev											# links the environment "lib-mgmt-dev" with the app "lib-mgmt"
	$ eb list
	
# Set EBS environment variables - Wait until environment is created
	$ eb setenv DATABASE_URL=mysql+mysqlconnector://root:password@<db_endpoint>:3306/mydb

# Deploy EB Project
	$ eb deploy
```

## 6. Endpoints and CURLs

| Method | Endpoint                                 | Description         |
|--------|------------------------------------------|---------------------|
| POST   | `/users/`                                | Create a new user   |
| GET    | `/users/`                                | List all users      |
| POST   | `/books/`                                | Create a new book   |
| GET    | `/books/`                                | List all books      |
| POST   | `/books/{book_id}/borrow/{user_id}`      | Borrow a book       |
| POST   | `/books/{book_id}/return/{user_id}`      | Return a book       |

Replace <URL>:<port> with your server address (e.g., http://localhost:8000)
```bash
# Create a new user
curl -X POST <URL>:<port>/users/ -H "Content-Type: application/json" -d '{"name": "Alice"}'

# List all users
curl <URL>:<port>/users/

# Create a new book
curl -X POST <URL>:<port>/books/ -H "Content-Type: application/json" -d '{"title": "1984", "author": "George Orwell"}'

# List all books
curl <URL>:<port>/books/

# Borrow a book (book_id=1, user_id=2)
curl -X POST <URL>:<port>/books/1/borrow/2

# Return a book (book_id=1, user_id=2)
curl -X POST <URL>:<port>/books/1/return/2
```

## 7. Project Structure

```bash
library-management/
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
├── .gitignore               # Git exclusions
├── application.py           # EBS entry point
├── diagram.png              # Architectural diagram for cloud
├── docker-compose.yml       # Multi-container orchestration
├── Procfile*                # EBS startup config: runs gunicorn with uvicorn for ASGI support
├── README.md
└── requirements.txt         # Python dependencies

Procfile Note: Elastic Beanstalk expects a WSGI-compatible interface, but FastAPI is ASGI-based. To bridge this, use Gunicorn with the Uvicorn worker to serve FastAPI properly.
```

## 8. Annex

Install AWS CLI and EBS CLI
```bash
# Install libraries and dependencies
	$ sudo apt update
	$ sudo apt install python3-pip python3-venv git unzip -y

# Install aws cli global
	$ curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
	$ unzip awscliv2.zip
	$ sudo ./aws/install
    $ aws --version

# Install ebs cli global with pipx
	$ sudo apt install pipx
	$ pipx ensurepath
	$ pipx install awsebcli
	$ echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
	$ source ~/.bashrc
	$ eb --version
```

Extra Commands
```bash
$ docker exec -it <container_name> mysql -u root -p		# Access container db (general command)
$ docker exec -it mysql_fastapi mysql -u root -p		# Access container db (example)
```
